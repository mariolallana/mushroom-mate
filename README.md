Run backend:
Open anaconda prompt and navigate to mushroom-mate folder
Run the virtual environment with the command: 
```bash
.\venv\Scripts\activate
```

If you don't have it create it and install the requirements.txt:

```bash
python -m venv venv
pip install -r requirements.txt
```

Then run the comand
```bash
python app.py
```

Run frontend:

Open CMD and run 
```bash
npm install
npm install react react-dom
npm install -D vite-plugin-react @vitejs/plugin-react-refresh tailwindcss@latest postcss@latest autoprefixer@latest

npm start

npm run dev
```
