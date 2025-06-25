import os
import json
import threading
import socket
import time

NODE_DIR = './domain1/Node'
BASE_PORT = 10000
NODE_COUNT = 20

global_done = threading.Event()
node_status = {}

# 读取所有节点配置
def load_nodes():
    nodes = []
    for i in range(1, NODE_COUNT + 1):
        file_path = os.path.join(NODE_DIR, f'node{i}.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            node = json.load(f)
            node['port'] = BASE_PORT + i - 1
            nodes.append(node)
    return nodes

# 节点服务线程
def node_server(node, nodes_dict):
    port = node['port']
    name = f"Node{node['id']}"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', port))
    print(f"{name} 启动在端口 {port}")
    sent = set()
    replied = set()
    # 启动后主动向所有邻居发送自己的节点号
    for adj in node['adjacent']:
        if adj in nodes_dict:
            adj_port = nodes_dict[adj]['port']
            s.sendto(f"hello from {name}".encode('utf-8'), ('127.0.0.1', adj_port))
            print(f"{name} 向 {adj} 发送成功")
            sent.add(adj)
    while len(replied) < len(sent):
        try:
            data, addr = s.recvfrom(1024)
            msg = data.decode('utf-8')
            # 收到消息后主动回发一次
            if not msg.startswith(f"hello from {name}"):
                s.sendto(f"hello from {name}".encode('utf-8'), addr)
            # 只显示一次收到回复
            for adj in sent:
                if adj in msg and adj not in replied:
                    print(f"{name} 收到来自 {adj} 的回复: {msg}")
                    replied.add(adj)
                    break
        except ConnectionResetError:
            continue
        # 检查未完成的邻居，重发
        for adj in sent - replied:
            if adj in nodes_dict:
                adj_port = nodes_dict[adj]['port']
                s.sendto(f"hello from {name}".encode('utf-8'), ('127.0.0.1', adj_port))
    node_status[name] = True
    s.close()
    # 检查所有节点是否都完成
    if all(node_status.get(f"Node{i}") for i in range(1, NODE_COUNT+1)):
        global_done.set()

def start_all_nodes():
    nodes = load_nodes()
    nodes_dict = {f"Node{n['id']}": n for n in nodes}
    for node in nodes:
        node_status[f"Node{node['id']}"] = False
    for node in nodes:
        t = threading.Thread(target=node_server, args=(node, nodes_dict), daemon=True)
        t.start()

        

if __name__ == '__main__':
    start_all_nodes()
    print("所有节点已启动，可通过UDP端口10000~10019互发消息")
    global_done.wait()
    print("所有邻接节点间通信已完成，端口已释放。程序退出。")
