# **About this project:**

Manga parser from website hentai-chan.me

What works:

1. Parsing all manga pages.
2. Downloading and unpacking manga archives.
3. Connecting to MongoDB database and adding mango to it

# Installation:

1. Clone repo

```
    $ git clone https://github.com/Fretrv/hchanme-parser.git
```

2. Create a virtual environment and activate it.

```
    $ cd hchanme-parser/
    $ python -m venv venv
```

Windows:

```
    $ .\venv\Scripts\activate.ps1
```

Linux:

```
    $ source ./venv/bin/activate
```

3. Install the required libraries.

```
    $ python3 -m pip install -r requirements.txt
```

# Usage

Run with command

```
    $ python main.py --mongodb mongodb://localhost:27017
```

where `mongodb://localhost:27017` URI link of your MongoDB database.
