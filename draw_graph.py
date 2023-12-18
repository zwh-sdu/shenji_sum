# -*- coding: utf-8 -*-

import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
import re


class HtmlWindow(QMainWindow):
    def __init__(self, nodes, links):
        super().__init__()
        self.nodes = nodes
        self.links = links
        self.initUI()

    def initUI(self):
        self.setWindowTitle('审计局政府会议知识图谱')
        self.setGeometry(100, 100, 800, 600)

        # 创建 QWebEngineView
        self.browser = QWebEngineView()

        # 定义 HTML 内容
        html_content = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>审计局政府会议知识图谱</title>
            <script>{d3_js_content}</script>
            <style>
                .links line {{
                    stroke: #999;
                    stroke-opacity: 0.6;
                }}

                .nodes circle {{
                    stroke: #fff;
                    stroke-width: 1.5px;
                }}

                text {{
                    font-family: sans-serif;
                    font-size: 10px;
                }}
            </style>
        </head>
        <body>
            <svg width="960" height="600"></svg>
            <script>
                // 内嵌的 JSON 数据
                const graph = {{
                  "nodes": {json.dumps(self.nodes)},
                  "links": {json.dumps(self.links)}
                }};

                // D3.js 代码
                const svg = d3.select("svg"),
                    width = +svg.attr("width"),
                    height = +svg.attr("height");

                const simulation = d3.forceSimulation()
                    .force("link", d3.forceLink().id(function(d) {{ return d.id; }}))
                    .force("charge", d3.forceManyBody())
                    .force("center", d3.forceCenter(width / 2, height / 2));

                const link = svg.append("g")
                    .attr("class", "links")
                    .selectAll("line")
                    .data(graph.links)
                    .enter().append("line");

                const node = svg.append("g")
                    .attr("class", "nodes")
                    .selectAll("g")
                    .data(graph.nodes)
                    .enter().append("g");

                const circles = node.append("circle")
                    .attr("r", 5)
                    .attr("fill", function(d) {{ return color(d.group); }})
                    .call(d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                        .on("end", dragended));

                const labels = node.append("text")
                    .text(function(d) {{
                        return d.id;
                    }})
                    .attr('x', 6)
                    .attr('y', 3);

                simulation
                    .nodes(graph.nodes)
                    .on("tick", ticked);

                simulation.force("link")
                    .links(graph.links);

                function ticked() {{
                    link
                        .attr("x1", function(d) {{ return d.source.x; }})
                        .attr("y1", function(d) {{ return d.source.y; }})
                        .attr("x2", function(d) {{ return d.target.x; }})
                        .attr("y2", function(d) {{ return d.target.y; }});

                    node
                        .attr("transform", function(d) {{
                            return "translate(" + d.x + "," + d.y + ")";
                        }});
                }}

                function dragstarted(d) {{
                    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                }}

                function dragged(d) {{
                    d.fx = d3.event.x;
                    d.fy = d3.event.y;
                }}

                function dragended(d) {{
                    if (!d3.event.active) simulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }}

                function color(group) {{
                    switch(group) {{
                        case 1: return "#1f77b4";
                        case 2: return "#2ca02c";
                        case 3: return "#ff7f0e";
                        default: return "#AA00BB";
                    }}
                }}
            </script>
        </body>
        </html>
        """

        # 渲染 HTML 内容
        self.browser.setHtml(html_content)

        # 设置浏览器为中心控件
        self.setCentralWidget(self.browser)


def get_nodes_and_lines(data):
    nodes = [
        {"id": data[0], "group": 1},  # 会议时间
        {"id": data[1], "group": 2}  # 会议名称
    ]
    links = [{"source": data[0], "target": data[1]}]

    # 事件
    event_money_list = data[3:]
    for event_money in event_money_list:
        event_money = event_money[event_money.index('.') + 1:].strip()
        event, money = list(map(lambda x: x.strip(), event_money.split('|')))
        nodes.append({"id": event, "group": 2})
        links.append({"source": data[1], "target": event})
        if bool(re.search(r'\d', money)):
            nodes.append({"id": money, "group": 3})
            links.append({"source": event, "target": money})

    return nodes, links


if __name__ == '__main__':
    with open('./output.txt', 'r', encoding='UTF-8') as f:
        data = f.readlines()

    app = QApplication(sys.argv)

    # 读取 d3.v5.min.js 文件
    with open('./d3.v5.min.js', 'r') as file:
        d3_js_content = file.read()

    nodes, links = get_nodes_and_lines(data)
    # print(links)
    # # 定义节点和连线
    # nodes = [
    #     {"id": "2023年11月15日", "group": 1},
    #     {"id": "2023年11月16日", "group": 1},
    #     {"id": "2023年11月17日", "group": 1},
    #     {"id": "北京市建设局会议室", "group": 1},
    #     {"id": "市政工程现场", "group": 1},
    #     {"id": "张华", "group": 2},
    #     {"id": "李伟", "group": 2},
    #     {"id": "赵敏", "group": 2},
    #     {"id": "王丽", "group": 2},
    #     {"id": "陈强", "group": 2},
    #     {"id": "刘洋", "group": 2},
    #     {"id": "项目规划讨论", "group": 3},
    #     {"id": "建筑设计审查", "group": 3},
    #     {"id": "工程进度汇报", "group": 3},
    #     {"id": "材料供应协调", "group": 3},
    #     {"id": "安全管理培训", "group": 3},
    #     {"id": "城市规划", "group": 4},
    #     {"id": "建筑材料", "group": 4},
    #     {"id": "工程质量控制", "group": 4},
    #     {"id": "项目管理", "group": 4},
    #     {"id": "施工技术", "group": 4},
    #     {"id": "环境保护", "group": 4},
    #     {"id": "预算控制", "group": 4},
    #     {"id": "法规遵守", "group": 4},
    #     {"id": "创新技术应用", "group": 4},
    #     {"id": "团队协作", "group": 4},
    #     {"id": "项目效率", "group": 4},
    #     {"id": "风险管理", "group": 4}
    # ]
    # links = [
    #     {"source": "2023年11月15日", "target": "张华"},
    #     {"source": "2023年11月16日", "target": "李伟"},
    #     {"source": "2023年11月17日", "target": "赵敏"},
    #     {"source": "北京市建设局会议室", "target": "王丽"},
    #     {"source": "市政工程现场", "target": "陈强"},
    #     {"source": "项目规划讨论", "target": "刘洋"},
    #     {"source": "建筑设计审查", "target": "张华"},
    #     {"source": "工程进度汇报", "target": "李伟"},
    #     {"source": "材料供应协调", "target": "赵敏"},
    #     {"source": "安全管理培训", "target": "王丽"},
    #     {"source": "城市规划", "target": "陈强"},
    #     {"source": "建筑材料", "target": "刘洋"},
    #     {"source": "工程质量控制", "target": "张华"},
    #     {"source": "项目管理", "target": "李伟"},
    #     {"source": "施工技术", "target": "赵敏"},
    #     {"source": "环境保护", "target": "王丽"},
    #     {"source": "预算控制", "target": "陈强"},
    #     {"source": "法规遵守", "target": "刘洋"},
    #     {"source": "创新技术应用", "target": "张华"},
    #     {"source": "团队协作", "target": "李伟"},
    #     {"source": "项目效率", "target": "赵敏"},
    #     {"source": "风险管理", "target": "王丽"},
    #     {"source": "张华", "target": "项目规划讨论"},
    #     {"source": "李伟", "target": "建筑设计审查"},
    #     {"source": "赵敏", "target": "工程进度汇报"},
    #     {"source": "王丽", "target": "材料供应协调"},
    #     {"source": "陈强", "target": "安全管理培训"},
    #     {"source": "刘洋", "target": "城市规划"},
    #     {"source": "项目规划讨论", "target": "建筑材料"},
    #     {"source": "建筑设计审查", "target": "工程质量控制"},
    #     {"source": "工程进度汇报", "target": "项目管理"},
    #     {"source": "材料供应协调", "target": "施工技术"},
    #     {"source": "安全管理培训", "target": "环境保护"},
    #     {"source": "城市规划", "target": "预算控制"},
    #     {"source": "建筑材料", "target": "法规遵守"},
    #     {"source": "工程质量控制", "target": "创新技术应用"},
    #     {"source": "项目管理", "target": "团队协作"},
    #     {"source": "施工技术", "target": "项目效率"},
    #     {"source": "环境保护", "target": "风险管理"}
    # ]

    ex = HtmlWindow(nodes, links)
    ex.show()
    sys.exit(app.exec_())
