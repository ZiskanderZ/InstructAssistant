import os
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun

from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain import hub

from config import open_ai_token

class AiSimpleClient:

    def __init__(self):

        os.environ["OPENAI_API_KEY"] = open_ai_token
        self.model = ChatOpenAI(model="gpt-3.5-turbo")

        self.tools = [CustomCalculatorTool()]

        self.prompt = hub.pull("hwchase17/openai-functions-agent")
        self.init_agent()
        

    def init_agent_from_promt(self, promt):

        self.prompt.messages[0].prompt.template = promt
        self.init_agent()


    def init_agent(self):

        
        self.store = {}
        agent = create_tool_calling_agent(self.model, self.tools, self.prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        
        self.agent_with_chat_history = RunnableWithMessageHistory(agent_executor, self.get_session_history,
                                                                  input_messages_key="input", history_messages_key="chat_history")
                                    

    def get_session_history(self, session_id: str) -> ChatMessageHistory:

        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]
    
    
    def get_config(self, id):

        return {"configurable": {"session_id": id}}
    

    def reply(self, question: str, id) -> any: 

        config = self.get_config(id)
        
        response = self.agent_with_chat_history.invoke({"input": [HumanMessage(content=question)]},
                                                    config=config)

        return response['output']
    

class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")

class CustomCalculatorTool(BaseTool):

    name = "Calculator"
    description = "useful for when you need to answer questions about math"
    args_schema: Type[BaseModel] = CalculatorInput
    # return_direct: bool = True

    def _run(self, a: int, b: int, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:

        """Use the tool."""

        return a * b

    def _arun(self, a: int, b: int, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:

        """Use the tool asynchronously."""

        raise NotImplementedError("Calculator does not support async")