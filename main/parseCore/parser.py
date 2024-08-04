import re
from bs4 import BeautifulSoup


import asyncio
import aiohttp
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError


def price_to_int(price: str):
    # Заменяем все пробелы (включая неразрывные) на пустую строку
    price = re.sub(r'\s+', '', price)

    # Заменяем все запятые на точки
    price = price.replace(',', '.')

    # Находим все числовые последовательности (включая десятичные точки)
    match = re.search(r'\d+(\.\d+)?', price)

    if match:
        number_str = match.group(0)
        # Преобразуем строку в float или int
        if '.' in number_str:
            return float(number_str)
        else:
            return int(number_str)
    else:
        return None


class AsyncParser:
    def __init__(self, delay: float = 0):
        self.delay = delay if delay > 0 else 0
        self.user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0')

    async def fetch(self, session: ClientSession, link: dict, tags_trail: str) -> dict:
        headers = {'User-Agent': self.user_agent}
        try:
            async with session.get(link['link'], headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                print(link['id'], link['link'])
                text = await response.text()
                price_tags = BeautifulSoup(text, 'html.parser').select(tags_trail)
                price = price_tags[0].text if price_tags else -1
                price = price_to_int(price)
                return {'id': link['id'], 'price': price}
        except (ClientConnectorError, aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Error fetching {link['link']}: {e}")
            return {'id': link['id'], 'price': -1}

    async def parse(self, links: list, tags_trail: str) -> list:
        async with aiohttp.ClientSession() as session:
            results = []
            for i in range(0, len(links), 5):  # Проходим по ссылкам с шагом 5
                chunk = links[i:i + 5]  # Получаем срез из 5 элементов
                tasks = []

                for link in chunk:
                    if self.delay > 0:
                        await asyncio.sleep(self.delay)
                    task = self.fetch(session, link, tags_trail)
                    tasks.append(task)

                # Ждем завершения всех задач в текущем срезе
                chunk_results = await asyncio.gather(*tasks)
                results.extend(chunk_results)  # Добавляем результаты в общий список

            return results
