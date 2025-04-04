LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="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"
LANGSMITH_PROJECT="SimplifyMoney"
OPENAI_API_KEY="<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>"


from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
llm.invoke("Hello, world!")
