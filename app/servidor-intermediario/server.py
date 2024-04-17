from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route('/scrape_wikipedia', methods=['POST'])
def scrape_wikipedia():
    try:
        search_term = request.form.get('search_term')
        wikipedia_url = f'https://en.wikipedia.org/wiki/{search_term}'

        response = requests.get(wikipedia_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the infobox-nowrap table
        infobox = soup.find('table', class_='infobox nowrap')

        if infobox:
            # Extract relevant data from the infobox
            # (e.g., food details, nutrition facts, etc.)
            # Process the data as needed

            # Example: Get the first row of the infobox
            rows = infobox.find_all('tr')
            first_row = rows[0].text.strip()
            
            return jsonify({'success': True, 'data': first_row})
        else:
            return jsonify({'success': False, 'message': 'No infobox nowrap found.'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)