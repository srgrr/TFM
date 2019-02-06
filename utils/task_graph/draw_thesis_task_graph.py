#!/usr/bin/python3
import pandas as pd

FILE_PATH = "time_estimations.csv"

def main():
  g = []

  with open(FILE_PATH, "r") as f:
    df = pd.read_csv(f, delimiter = ",", dtype = str)
    for (i, line) in df.iterrows():
      dep_line = line["Dependencies"].replace("no", "")
      cur_node = {
        "name": "%s (%s)\\n%s" % (line["Name"], line["Time"], line["Comment"]),
        "cost": int(line["Time"]),
        "edges": [x - 2 for x in list(map(int, dep_line.split()))]
      }
      g.append(cur_node)

  print("digraph thesis_tasks {")
  print("rankdir=LR;")
  print("\tnode [shape = circle]; %s ;" % " ".join("\"%s\"" % x["name"] for x in g))

  vis = [False] * len(g)

  def dfs(i):
    if vis[i]: return
    vis[i] = True
    for edge in g[i]["edges"]:
      adj = g[edge]
      print(
        "\t\"%s\" -> \"%s\"" % (adj["name"], g[i]["name"])
      )
      dfs(edge)

  for (i, v) in enumerate(g):
      dfs(i)

  print("}")


if __name__ == "__main__":
  main()
