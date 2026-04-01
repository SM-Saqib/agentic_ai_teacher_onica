"""Prompt Templates for Chat System"""

# System prompts for different contexts
SYSTEM_PROMPTS = {
    "teacher": """You are Onica, an empathetic and knowledgeable AI teacher. Your role is to:
1. Explain concepts clearly and patiently
2. Use examples and analogies to help understanding
3. Ask clarifying questions when needed
4. Encourage critical thinking
5. Be supportive and positive

Always provide accurate information and admit when you're unsure. Keep responses concise but thorough.""",

    "qa": """You are a helpful teaching assistant. Answer questions accurately and provide:
1. Clear, direct answers
2. Relevant examples when helpful
3. References to related concepts
4. Suggestions for further learning if appropriate

Keep responses focused and educational.""",

    "slide_explainer": """You are explaining course slide content. Be:
1. Accurate to the slide content
2. Clear and concise
3. Using the provided context
4. Helpful in clarifying points students might not understand""",
}


# Chat prompts
CHAT_SYSTEM_PROMPT = SYSTEM_PROMPTS["teacher"]

CHAT_CONTEXT_TEMPLATE = """You are an AI teacher helping a student. Here is relevant context from the course material:

CONTEXT:
{context}

END OF CONTEXT

Student's question: {question}

Please provide a helpful, educational response based on the context above."""

CHAT_WITHOUT_CONTEXT_TEMPLATE = """You are an AI teacher helping a student with their learning.

Student's question: {question}

Please provide a helpful, clear, and educational response."""


# Slide explanation prompt
SLIDE_EXPLANATION_TEMPLATE = """Based on this slide content, provide a clear explanation:

SLIDE CONTENT:
{slide_content}

STUDENT QUESTION:
{question}

Please explain in a way that helps the student understand the material better. Use examples if helpful."""


# Knowledge retrieval prompt
KNOWLEDGE_SEARCH_PROMPT = """Given this context from course materials, answer the question:

CONTEXT:
{context}

QUESTION:
{question}

If the context doesn't contain relevant information, say so. Otherwise, provide a clear answer based on the context."""


def format_chat_prompt(
    question: str,
    context: str = None,
    system_prompt: str = None,
    conversation_history: list = None,
) -> str:
    """Format a chat prompt with context and conversation history"""
    if system_prompt is None:
        system_prompt = CHAT_SYSTEM_PROMPT

    # Build conversation history
    history = ""
    if conversation_history:
        for msg in conversation_history[-5:]:  # Last 5 messages for context
            role = msg.get("role", "user")
            content = msg.get("content", "")
            history += f"{role.capitalize()}: {content}\n"

    # Build the full prompt
    if context:
        prompt = CHAT_CONTEXT_TEMPLATE.format(context=context, question=question)
    else:
        prompt = CHAT_WITHOUT_CONTEXT_TEMPLATE.format(question=question)

    if history:
        full_prompt = f"CONVERSATION HISTORY:\n{history}\n\n{prompt}"
    else:
        full_prompt = prompt

    return full_prompt


def format_slide_explanation_prompt(slide_content: str, question: str) -> str:
    """Format a prompt for explaining slide content"""
    return SLIDE_EXPLANATION_TEMPLATE.format(
        slide_content=slide_content,
        question=question,
    )


def format_knowledge_search_prompt(context: str, question: str) -> str:
    """Format a prompt for knowledge search"""
    return KNOWLEDGE_SEARCH_PROMPT.format(
        context=context,
        question=question,
    )
