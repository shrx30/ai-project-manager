from app.graph import graph


result = graph.invoke(
    {
        "repository": "fastapi/fastapi",
        "issues": [],
        "analysis": "",
    }
)

print("\n===== PROJECT ANALYSIS =====\n")
print(result["analysis"])