

from c_json import GlobalConfig
config=GlobalConfig()
config.load_from_file('config.json')
print(f"当前模块: {__name__}, config id: {id(config)}, config.name: {config.name}")

def start_main_important_data():
    if config.name == "main.py":
        with open("important_data.txt", "w", encoding='utf8') as f:
            pass

def write_main_important_data(string):
    if config.name=="main.py":
        with open("important_data.txt" ,"a" ,encoding='utf8') as f:
            f.write(string)