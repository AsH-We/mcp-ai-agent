import re
import json
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.language_models import BaseChatModel


class RuleBasedMockLLM(BaseChatModel):
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        last_msg_obj = messages[-1]

        if hasattr(last_msg_obj, "tool_call_id") or last_msg_obj.type == "tool":
            raw_content = last_msg_obj.content
            print(f"DEBUG: Tool output detected: {raw_content}")

            try:
                data = json.loads(raw_content.replace("'", '"'))

                if "status" in data and data["status"] == "added":
                    human_text = f"Продукт '{data['name']}' успешно добавлен в базу под ID {data['id']}."

                elif "total_products" in data:
                    human_text = (f"Статистика базы:\n"
                                  f"- Всего товаров: {data['total_products']}\n"
                                  f"- Средняя цена: {data['average_price']:.2f} руб.")

                elif isinstance(data, list):
                    human_text = "Список доступных продуктов:\n" + "\n".join(
                        [f"- {p['name']} ({p['price']} руб.)" for p in data]
                    )

                else:
                    human_text = raw_content

            except Exception as e:
                print(f"DEBUG: Formatting error: {e}")
                human_text = raw_content

            return ChatResult(generations=[ChatGeneration(message=AIMessage(content=human_text))])

        last_msg = last_msg_obj.content.lower()
        print(f"DEBUG: Processing query: '{last_msg}'")

        tool_calls = []

        # 1. Список продуктов
        if "покажи" in last_msg and "продукт" in last_msg:
            print("DEBUG: Matched 'list_products'")
            tool_calls.append({
                "name": "list_products",
                "args": {},
                "id": "call_1"
            })

        # 2. Статистика
        elif "средняя" in last_msg or "статистик" in last_msg:
            print("DEBUG: Matched 'get_statistics'")
            tool_calls.append({
                "name": "get_statistics",
                "args": {},
                "id": "call_2"
            })

        # 3. Добавление продукта
        elif "добавь" in last_msg:
            print("DEBUG: Attempting to parse 'add_product'")
            try:
                name_match = re.search(r"продукт[:\s]+(.+?)(?:,|$|\sцена)", last_msg)
                price_match = re.search(r"цена\s*[:]?\s*(\d+)", last_msg)
                cat_match = re.search(r"категория\s*[:]?\s*([A-Za-zА-Яа-я0-9\s]+)", last_msg)

                if name_match and price_match and cat_match:
                    name = name_match.group(1).replace(":", "").strip()
                    price = float(price_match.group(1))
                    category = cat_match.group(1).strip()

                    print(f"DEBUG: Parsed - Name: {name}, Price: {price}, Category: {category}")

                    tool_calls.append({
                        "name": "add_product",
                        "args": {
                            "name": name,
                            "price": price,
                            "category": category
                        },
                        "id": "call_3"
                    })
                else:
                    print(
                        f"DEBUG: Parsing failed. Name: {bool(name_match)}, Price: {bool(price_match)}, Cat: {bool(cat_match)}")
            except Exception as e:
                print(f"DEBUG: Exception during parsing: {e}")

        # 4. Скидка
        elif "скидк" in last_msg and "id" in last_msg:
            print("DEBUG: Matched 'calculate_discount'")
            id_match = re.search(r"id\s*[:]?\s*(\d+)", last_msg)
            percent_match = re.search(r"(\d+)%", last_msg)
            if id_match and percent_match:
                tool_calls.append({
                    "name": "calculate_discount",
                    "args": {
                        "product_id": int(id_match.group(1)),
                        "discount_percent": float(percent_match.group(1))
                    },
                    "id": "call_4"
                })

        content = "" if tool_calls else "Я не понял запрос. Попробуйте переформулировать (проверьте формат: 'Добавь продукт: Имя, цена 100, категория Тест')."

        msg = AIMessage(content=content, tool_calls=tool_calls)
        return ChatResult(generations=[ChatGeneration(message=msg)])

    @property
    def _llm_type(self) -> str:
        return "mock-rule-based"