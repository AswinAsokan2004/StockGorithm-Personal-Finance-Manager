import requests

def fetch_sentiment():
    try:
        url = "https://9efa-2401-4900-646d-edfb-dca9-a20e-4626-28f8.ngrok-free.app//sentiment"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            print("News Headline + Description:\n", data["news"])
            print("Sentiment Result:")
            for i, sentiment in enumerate(data["sentiment"]):
                print(f"  News {i+1}:")
                print(f"    Label: {sentiment['label']}")
                print(f"    Confidence Score: {sentiment['score']}")
                print('data is:',data)
            return data
        else:
            print("Error:", data.get("error"))

    except Exception as e:
        print("Request failed:", str(e))
