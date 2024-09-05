from django.shortcuts import render, redirect
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import io

def get_tables_from_url(url):
    # Set up Selenium with headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    service = Service('C:/webdriver/chromedriver.exe')  # Update with your path
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Navigate to the provided URL
    driver.get(url)

    # Find all tables on the page
    tables = driver.find_elements(By.TAG_NAME, 'table')

    table_data = []
    for index, table in enumerate(tables):
        rows = table.find_elements(By.TAG_NAME, 'tr')

        # Extract table rows into a list of lists
        table_rows = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')  # Find all cells in the row
            row_data = [cell.text for cell in cells]  # Extract text from each cell
            table_rows.append(row_data)

        table_data.append({
            'index': index,  # The table index (starts from 0)
            'rows': table_rows
        })

    driver.quit()  # Close the browser when done
    return table_data

def url_input(request):
    return render(request, 'url_input.html')  # Form to input URL

def fetch_tables(request):
    if request.method == 'POST':
        url = request.POST.get('url')  # Get URL from the form
        if not url:
            return HttpResponse("Please enter a valid URL.")

        try:
            table_data = get_tables_from_url(url)  # Fetch tables using Selenium
            if not table_data:
                return HttpResponse("No tables found on this page.")

            # Pass the adjusted index to the template
            for table in table_data:
                table['adjusted_index'] = table['index'] 

            return render(request, 'list.html', {'table_data': table_data, 'url': url})

        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")
    return redirect('url_input')  # Redirect to URL input if not POST


def download_table(request):
    url = request.GET.get('url')  # Get the URL from the request
    table_index = int(request.GET.get('table_index', 0))  # Get the selected table index

    # Fetch tables from the given URL
    table_data = get_tables_from_url(url)
    selected_table = table_data[table_index]  # Get the requested table by index

    # Convert the table's rows to a DataFrame
    df = pd.DataFrame(selected_table['rows'])

    # Create CSV in memory
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    # Send CSV file as a response
    response = HttpResponse(buffer, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=table_{table_index}.csv'

    return response
