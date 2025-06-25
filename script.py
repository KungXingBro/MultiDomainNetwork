import os
import json
import random
import string

node_dir = os.path.join("./domain1/")
os.makedirs(node_dir, exist_ok=True)

# 获取domain文件夹下的所有节点配置的id字段
all_nodes_id = []
for root, dirs, files in os.walk(node_dir):
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    node_data = json.load(f)
                    all_nodes_id.append(node_data['id'])
            except json.JSONDecodeError:
                print(f"无法解析文件 {file_path}，请检查文件格式。")

print(all_nodes_id)


def random_str(length=20):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_user(length=3):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

for i in range(1, 21):
    candidates = [n for n in all_nodes_id if n != f"Node{i}"]
    adjacent = random.sample(candidates, random.randint(3, 6))
    server = None if random.random() < 0.3 else random_str(20)
    user_count = random.randint(1, 5)
    users = [random_user(3) for _ in range(user_count)]
    node_data = {
        "id": "normal-node%d" % i,
        "server": server,
        "user": users,
        "adjacent": adjacent
    }
    file_path = os.path.join("./domain1/Node/",  f"node{i}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(node_data, f, ensure_ascii=False, indent=4)
    print(f"已生成节点配置文件：{file_path}")
