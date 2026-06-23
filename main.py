import asyncio

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import KernelArguments
from semantic_kernel.filters import PromptRenderContext, FilterTypes

system_message = """
You are a chat bot. Your name is MJBot.
"""


async def prompt_rendering_filter(context: PromptRenderContext, next):
    print("Before Rendering...")

    await next(context)

    print("After Rendering...")

    context.rendered_prompt = f"In case you found any city names, just say, I can answer about counties and not city like 'Just give me a country name and not city' {context.rendered_prompt or ''}"


kernel = Kernel()
service_id = "chat-gpt"
kernel.add_service(AzureChatCompletion(service_id=service_id))
kernel.add_filter(FilterTypes.PROMPT_RENDERING, prompt_rendering_filter)

settings = kernel.get_prompt_execution_settings_from_service_id(service_id)

chat_function = kernel.add_function(
    plugin_name="ChatBot",
    function_name="Chat",
    prompt="{{$chat_history}}{{$user_input}}",
    template_format="semantic-kernel",
    prompt_execution_settings=settings,
)

chat_history = ChatHistory(system_message=system_message)
chat_history.add_user_message("Hi there, who are you?")


async def chat() -> bool:
    user_input = input("User:> ")

    if user_input == "exit":
        return False

    answer = await kernel.invoke(
        chat_function,
        KernelArguments(
            user_input=user_input,
            chat_history=chat_history,
        ),
    )
    chat_history.add_user_message(user_input)
    chat_history.add_assistant_message(str(answer))
    print(f"MJBot:> {answer}")
    return True


async def main() -> None:
    chatting = True
    while chatting:
        chatting = await chat()


if __name__ == "__main__":
    asyncio.run(main())
