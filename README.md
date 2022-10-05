# Upwork. Upload images to dropbox and generate csv

### setup your dropbox

#### 1. Go to https://www.dropbox.com/developers/apps?_tk=pilot_lp&_ad=topbar4&_camp=myapps and create your app
#### 2. Go to permissions of your app and add files.content.write scope
#### 3. Click button Generate token and copy it
#### 4. Open app.env and fill DROPBOX_SECRET

### installation

#### 1. create virtualenv and activate it
```bash
    python3 -m venv && source venv/bin/activate
```
#### 2. install requirements
```bash
    pip install -r requirements.txt
```
#### 3. Create "images" directory in the root of project
#### 4. Put your images into ./images folder
#### 5. run script and wait
```bash
    python main.py
```
