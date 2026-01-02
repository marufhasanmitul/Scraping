from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# যে লিঙ্কগুলো আমরা স্ক্র্যাপ করতে চাই
urls = [
    "https://quotes.toscrape.com/",
    "https://quotes.toscrape.com/tag/love/",
    "https://quotes.toscrape.com/tag/life/",
    "https://quotes.toscrape.com/tag/books/"
    "https://quotes.toscrape.com/tag/friendship/"
    "https://quotes.toscrape.com/tag/simile/"
]


def get_all_quotes():
    all_data = []

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # প্রতিটি পেজ থেকে ক্যাটাগরি বা ট্যাগ খুঁজে বের করা (ঐচ্ছিক)
        # যেমন: হোম পেজ হলে 'General', ট্যাগ পেজ হলে ট্যাগের নাম
        tag_name = url.split('/')[-2] if 'tag' in url else 'General'

        quotes = soup.find_all('div', class_='quote')

        for q in quotes:
            text = q.find('span', class_='text').text
            author = q.find('small', class_='author').text

            all_data.append({
                'quote': text,
                'author': author,
                'category': tag_name
            })

    return all_data


@app.route('/api/all-quotes', methods=['GET'])
def quotes_api():
    data = get_all_quotes()
    return jsonify({
        "total_quotes": len(data),
        "data": data
    })


if __name__ == '__main__':
    app.run(debug=True)
