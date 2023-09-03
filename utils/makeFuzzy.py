class MakeFuzzy:
    def __init__(self):
        pass

    def execute(self, query_text:str):
        query_text_list = self.splitQueryText(query_text=query_text)
        fuzzy_query_text_list = self.addFuzzies(query_text_list=query_text_list)
        fuzzy_query_text = self.reassembleQueryTest(fuzzy_query_text_list=fuzzy_query_text_list)

        return fuzzy_query_text

    def splitQueryText(self, query_text:str) -> list:
        query_text_list = query_text.split()

        return query_text_list

    def addFuzzies(self, query_text_list:list) -> list:
        fuzzyLambda = lambda word: f"%{word}%"
        fuzzy_query_text_list = list(map(fuzzyLambda, query_text_list))

        return fuzzy_query_text_list

    def reassembleQueryTest(self, fuzzy_query_text_list:list) -> str:
        fuzzy_query_text = " ".join(fuzzy_query_text_list)
        
        return fuzzy_query_text

    