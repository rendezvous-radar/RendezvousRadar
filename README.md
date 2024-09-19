# 📌 Rendezvous Radar

This app allows users to search for activities. Users can manually select activity categories or input a text prompt, which is analyzed by a custom classification model to generate relevant results.

This app gets POIs, its data, and creates the map using the OpenStreetMap (OSM) API, geocodes and reverse geocodes using the Nominatim API, and a trained multi-label BERT classification model to predict activity categories based on user input.

## 🪄 Features

Users can:

- Search for POIs within a range of an address
- Type in a prompt to have the AI predict the POIs of interest
- Interact with the map and see information about each POI

## 📸 Screenshots

![Home Screen](home.png)
![Map Screen](map.png)

## Run Locally

Install Git LFS

```bash
  git lfs install
```

Clone the project

```bash
  git clone git@github.com:rendezvous-radar/RendezvousRadar.git
```

Go to the project directory

```bash
  cd RendezvousRadar
```

Go to the frontend directory

```bash
  cd frontend
```

Install dependencies

```bash
  npm install
```

Start the server

```bash
  npm run dev
```

In another window in the project open the backend directory

```bash
  cd backend
```

Create a virtual environment

```bash
  python -m venv venv
```

Activate the virtual environment

```bash
  # Linux/Mac
  source venv/bin/activate
  # Windows
  venv\Scripts\activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Apply migrations

```bash
  python manage.py migrate
```

Run the dev server

```bash
  python manage.py runserver
```

## 🔗 Links

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jinha-kim/)

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jerry-chen-8852a324b/)

## License

[MIT](https://choosealicense.com/licenses/mit/)
