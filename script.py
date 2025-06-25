import os
import json
import random
import string

node_dir = os.path.join("./domain1/Node")
os.makedirs(node_dir, exist_ok=True)

all_nodes = [f"Node{i}" for i in range(1, 21)] + ["bg", "rm"]

def random_str(length=20):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_user(length=3):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

for i in range(1, 21):
    candidates = [n for n in all_nodes if n != f"Node{i}"]
    adjacent = random.sample(candidates, random.randint(3, 6))
    server = None if random.random() < 0.3 else random_str(20)
    user_count = random.randint(1, 5)
    users = [random_user(3) for _ in range(user_count)]
    node_data = {
        "id": i,
        "server": server,
        "user": users,
        "adjacent": adjacent
    }
    file_path = os.path.join(node_dir, f"node{i}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(node_data, f, ensure_ascii=False, indent=4)
    print(f"已生成节点配置文件：{file_path}")
