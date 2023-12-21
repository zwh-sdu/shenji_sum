# -*- coding: utf-8 -*-
import argparse
import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
import re

from merge_node_and_link import *


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


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--file_dir", default="./data/llm_output", type=str, help="大模型抽取结果的 txt 所在目录")
    parser.add_argument("--d_threshold", default=5, type=int, help="编辑距离阈值")
    args = parser.parse_args()

    d_threshold = args.d_threshold
    file_dir = args.file_dir
    all_files = get_all_files_in_folder(file_dir)
    print("file num", len(all_files))

    all_nodes = []
    all_links = []
    for file in all_files:
        nodes, links = get_nodes_and_lines(file)
        all_nodes += nodes
        all_links += links

    nodes, links, merge_map = merge(all_nodes, all_links, d_threshold)
    print('node num', len(nodes))
    print('link num', len(links))
    print('merge_map', merge_map)

    app = QApplication(sys.argv)
    # 读取 d3.v5.min.js 文件
    with open('assets/d3.v5.min.js', 'r') as file:
        d3_js_content = file.read()
    ex = HtmlWindow(nodes, links)
    ex.show()
    sys.exit(app.exec_())
