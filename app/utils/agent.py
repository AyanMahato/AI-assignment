from .search_api import query_scraper_api
from .llm_handler import process_with_llm

def orchestrate_query(df, query_template):
    results = []
    for index, row in df.iterrows():
        str=query_template[(query_template.index("{")+1):query_template.index("}")]
        entity = row[str]
        search_results = query_scraper_api(query_template.format(**{str: entity}))
        extracted_data = process_with_llm(query_template, search_results)
        results.append({"company": entity, "result": extracted_data})
    return pd.DataFrame(results)
