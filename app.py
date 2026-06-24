from backend import (
    chatbot,
    get_all_threads,
    ingest_rag_document
)

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)

from langgraph.types import Command

import streamlit as st
import uuid
import tempfile
import os


# ========================= Dark Terminal CSS =========================

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', ui-monospace, monospace !important;
}

[data-testid="stAppViewContainer"] { background: #080a12 !important; }
[data-testid="stMain"] { background: #080a12 !important; }
.main .block-container {
    background: #080a12 !important;
    padding-top: 1rem !important;
    max-width: 860px;
}

[data-testid="stSidebar"] {
    background: #0d0f17 !important;
    border-right: 1px solid #1e2030 !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 4px !important; }

[data-testid="stSidebar"] .stButton button {
    width: 100% !important;
    text-align: left !important;
    font-size: 11px !important;
    font-family: 'JetBrains Mono', monospace !important;
    padding: 7px 10px !important;
    border-radius: 6px !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    color: #4a4c60 !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    transition: all .15s;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: #111325 !important;
    color: #9a9bb5 !important;
    border-color: #1e2030 !important;
}

.new-session-btn button {
    background: transparent !important;
    color: #7F77DD !important;
    border: 1px solid #7F77DD !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
    transition: background .15s !important;
}
.new-session-btn button:hover { background: #1a1b2e !important; }

hr { border-color: #1e2030 !important; margin: 8px 0 !important; }

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 4px 0 !important;
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
    font-size: 13px !important;
    line-height: 1.65 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

[data-testid="stChatMessage"][data-message-author-role="user"]
    [data-testid="stMarkdownContainer"] {
    background: #0a1a14 !important;
    border: 1px solid #0F6E56 !important;
    border-radius: 8px 8px 2px 8px !important;
    padding: 10px 14px !important;
    color: #5DCAA5 !important;
}

[data-testid="stChatMessage"][data-message-author-role="assistant"]
    [data-testid="stMarkdownContainer"] {
    background: #0d0f1a !important;
    border: 1px solid #1e2030 !important;
    border-radius: 2px 8px 8px 8px !important;
    padding: 10px 14px !important;
    color: #b0b1cc !important;
}

[data-testid="stStatus"] {
    background: #0d0f17 !important;
    border: 1px solid #1e2030 !important;
    border-radius: 6px !important;
    font-size: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
    color: #4a4c60 !important;
}

[data-testid="stAlert"] {
    background: #12100a !important;
    border: 1px solid #854F0B !important;
    border-radius: 8px !important;
    border-left: 3px solid #EF9F27 !important;
    font-size: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
    color: #EF9F27 !important;
}

.approve-btn button {
    background: #04342C !important;
    color: #1D9E75 !important;
    border: 1px solid #1D9E75 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    border-radius: 6px !important;
    transition: background .15s !important;
}
.approve-btn button:hover { background: #0F6E56 !important; color: #9FE1CB !important; }

.reject-btn button {
    background: transparent !important;
    color: #3a3c4e !important;
    border: 1px solid #1e2030 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    border-radius: 6px !important;
    transition: background .15s !important;
}
.reject-btn button:hover { background: #111325 !important; color: #9a9bb5 !important; }

[data-testid="stChatInput"] textarea {
    background: #0d0f17 !important;
    border: 1px solid #1e2030 !important;
    border-radius: 8px !important;
    color: #b0b1cc !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #3a3c4e !important; }
[data-testid="stChatInput"] {
    background: #0d0f17 !important;
    border: 1px solid #1e2030 !important;
    border-radius: 8px !important;
}

[data-testid="stSpinner"] p {
    font-size: 12px !important;
    color: #4a4c60 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

[data-testid="stToast"] {
    background: #0d0f17 !important;
    border: 1px solid #1e2030 !important;
    border-radius: 8px !important;
    color: #b0b1cc !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
}

[data-testid="stException"] {
    background: #120a0a !important;
    border: 1px solid #A32D2D !important;
    border-radius: 8px !important;
    color: #E24B4A !important;
    font-family: 'JetBrains Mono', monospace !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #1e2030; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #2a2c40; }
</style>
"""


# ========================= Helper functions =========================

def generate_thread_id():
    return str(uuid.uuid4())


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def get_thread_title(thread_id):
    """Return a human-readable title for a thread.

    Priority:
    1. Cached title already stored in session state.
    2. First user message found in the saved LangGraph checkpoint.
    3. Fallback placeholder.
    """
    titles = st.session_state.setdefault("thread_titles", {})
    if thread_id in titles:
        return titles[thread_id]

    # Try to load the first user message from the checkpoint
    try:
        state = chatbot.get_state(
            config={"configurable": {"thread_id": thread_id}}
        )
        messages = state.values.get("messages", [])
        for msg in messages:
            if isinstance(msg, HumanMessage) and msg.content:
                title = _truncate(str(msg.content))
                titles[thread_id] = title
                return title
    except Exception:
        pass

    return "new conversation"


def set_thread_title(thread_id, text):
    """Cache a human-readable title for a thread (from the first user message)."""
    titles = st.session_state.setdefault("thread_titles", {})
    if thread_id not in titles and text:
        titles[thread_id] = _truncate(text)


def _truncate(text, max_chars=32):
    """Shorten text to fit neatly in the sidebar."""
    text = text.strip().replace("\n", " ")
    return text if len(text) <= max_chars else text[:max_chars].rstrip() + "…"


def reset_chat():
    st.session_state["thread_id"] = generate_thread_id()
    st.session_state["message_history"] = []
    st.session_state["pending_hitl"] = None
    add_thread(st.session_state["thread_id"])


def load_conversation(thread_id):
    state = chatbot.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )
    return state.values.get("messages", [])


# ========================= HITL helper functions =========================

def get_pending_interrupt(thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    try:
        state_snapshot = chatbot.get_state(config)
        direct_interrupts = getattr(state_snapshot, "interrupts", ()) or ()
        if direct_interrupts:
            return direct_interrupts[0]
        tasks = getattr(state_snapshot, "tasks", ()) or ()
        for task in tasks:
            task_interrupts = getattr(task, "interrupts", ()) or ()
            if task_interrupts:
                return task_interrupts[0]
    except Exception:
        return None
    return None


def save_pending_interrupt(thread_id, interrupt_object):
    st.session_state["pending_hitl"] = {
        "thread_id": thread_id,
        "prompt": str(interrupt_object.value)
    }


def sync_pending_interrupt(thread_id):
    pending_interrupt = get_pending_interrupt(thread_id)
    if pending_interrupt is not None:
        save_pending_interrupt(thread_id, pending_interrupt)
    else:
        current_pending = st.session_state.get("pending_hitl")
        if (
            current_pending is not None
            and current_pending.get("thread_id") == thread_id
        ):
            st.session_state["pending_hitl"] = None


def resume_hitl_execution(decision):
    pending_hitl = st.session_state.get("pending_hitl")
    if not pending_hitl:
        st.warning("No pending action to approve or reject.")
        return

    interrupted_thread_id = pending_hitl["thread_id"]
    resume_config = {
        "configurable": {"thread_id": interrupted_thread_id},
        "metadata": {"thread_id": interrupted_thread_id},
        "run_name": "hitl_resume_trace",
    }

    try:
        with st.chat_message("assistant"):
            status_holder = {
                "box": st.status("↻ resuming execution...", expanded=True)
            }

            def resumed_ai_only_stream():
                for message_chunk, metadata in chatbot.stream(
                    Command(resume=decision),
                    config=resume_config,
                    stream_mode="messages",
                ):
                    if isinstance(message_chunk, ToolMessage):
                        tool_name = getattr(message_chunk, "name", "tool")
                        status_holder["box"].update(
                            label=f"⚙ tool :: {tool_name}",
                            state="running",
                            expanded=True,
                        )
                    if isinstance(message_chunk, AIMessage):
                        if message_chunk.content:
                            yield message_chunk.content

            resumed_ai_message = st.write_stream(resumed_ai_only_stream())

            next_interrupt = get_pending_interrupt(interrupted_thread_id)
            if next_interrupt is not None:
                save_pending_interrupt(interrupted_thread_id, next_interrupt)
                status_holder["box"].update(
                    label="⚠ another approval required",
                    state="complete",
                    expanded=False
                )
            else:
                st.session_state["pending_hitl"] = None
                status_holder["box"].update(
                    label="✓ execution complete",
                    state="complete",
                    expanded=False
                )

        if resumed_ai_message:
            st.session_state["message_history"].append({
                "role": "assistant",
                "content": resumed_ai_message
            })

        st.rerun()

    except Exception as error:
        st.error(f"[error] could not resume: {error}")


# ========================= Page setup =========================

st.set_page_config(
    page_title="NeuralChat · Agentic",
    page_icon="🤖",
    layout="wide"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Session state init ──
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = get_all_threads()

if "pending_hitl" not in st.session_state:
    st.session_state["pending_hitl"] = None

if "thread_titles" not in st.session_state:
    st.session_state["thread_titles"] = {}

add_thread(st.session_state["thread_id"])
sync_pending_interrupt(st.session_state["thread_id"])


# ========================= Sidebar =========================

with st.sidebar:

    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:4px 2px 16px;
                border-bottom:1px solid #1e2030;margin-bottom:12px">
        <div style="width:32px;height:32px;border-radius:8px;background:#7F77DD;
                    display:flex;align-items:center;justify-content:center;font-size:16px">🤖</div>
        <div>
            <div style="font-size:13px;font-weight:600;color:#c8c8d4;
                        font-family:'JetBrains Mono',monospace">NeuralChat</div>
            <div style="font-size:10px;color:#3a3c4e;
                        font-family:'JetBrains Mono',monospace">LangGraph · RAG · HITL</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="new-session-btn">', unsafe_allow_html=True)
    if st.button("+ new session", use_container_width=True):
        reset_chat()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:10px;color:#3a3c4e;text-transform:uppercase;
                letter-spacing:.1em;padding:14px 2px 6px;
                font-family:'JetBrains Mono',monospace">Sessions</div>
    """, unsafe_allow_html=True)

    for thread_id in st.session_state["chat_threads"][::-1]:
        # Use human-readable title instead of raw UUID
        label = "› " + get_thread_title(thread_id)

        if st.button(label, key=thread_id, use_container_width=True):
            st.session_state["thread_id"] = thread_id
            messages = load_conversation(thread_id)
            temp_messages = []
            for message in messages:
                if isinstance(message, HumanMessage):
                    role = "user"
                elif isinstance(message, AIMessage):
                    role = "assistant"
                else:
                    continue
                temp_messages.append({"role": role, "content": message.content})
            st.session_state["message_history"] = temp_messages
            sync_pending_interrupt(thread_id)
            st.rerun()


# ========================= Main area header =========================

st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:0 0 16px;border-bottom:1px solid #1e2030;margin-bottom:20px">
    <div style="display:flex;align-items:center;gap:10px">
        <div style="width:8px;height:8px;border-radius:50%;background:#1D9E75;flex-shrink:0"></div>
        <div>
            <div style="font-size:15px;font-weight:600;color:#c8c8d4;
                        font-family:'JetBrains Mono',monospace">Agentic Chatbot</div>
            <div style="font-size:10px;color:#3a3c4e;margin-top:1px;
                        font-family:'JetBrains Mono',monospace">RAG · HITL · streaming</div>
        </div>
    </div>
    <div style="font-size:10px;padding:3px 10px;border-radius:99px;
                background:#111325;color:#7F77DD;border:1px solid #2a2c40;
                font-family:'JetBrains Mono',monospace">● langgraph online</div>
</div>
""", unsafe_allow_html=True)


# ========================= Message history =========================

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ========================= HITL approval interface =========================

pending_hitl = st.session_state.get("pending_hitl")
current_thread_has_pending_hitl = (
    pending_hitl is not None
    and pending_hitl.get("thread_id") == st.session_state["thread_id"]
)

if current_thread_has_pending_hitl:
    st.warning(
        f"**[ HITL ] human approval required**\n\n"
        f"`{pending_hitl['prompt']}`"
    )

    approve_col, reject_col, _ = st.columns([1, 1, 3])

    with approve_col:
        st.markdown('<div class="approve-btn">', unsafe_allow_html=True)
        if st.button(
            "✓ approve",
            key=f"approve_{st.session_state['thread_id']}",
            use_container_width=True
        ):
            resume_hitl_execution("yes")
        st.markdown('</div>', unsafe_allow_html=True)

    with reject_col:
        st.markdown('<div class="reject-btn">', unsafe_allow_html=True)
        if st.button(
            "✗ reject",
            key=f"reject_{st.session_state['thread_id']}",
            use_container_width=True
        ):
            resume_hitl_execution("no")
        st.markdown('</div>', unsafe_allow_html=True)


# ========================= Chat input =========================

submission = st.chat_input(
    "send a message or attach a pdf…",
    accept_file=True,
    file_type=["pdf"],
    disabled=current_thread_has_pending_hitl
)

user_input = None

if submission:
    user_input = submission.text
    uploaded_files = submission.files

    if uploaded_files:
        uploaded_pdf = uploaded_files[0]
        temporary_file_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_pdf.getvalue())
                temporary_file_path = tmp.name

            with st.spinner(f"[rag] indexing {uploaded_pdf.name}…"):
                ingest_rag_document(temporary_file_path)

            st.toast(f"[rag] {uploaded_pdf.name} ingested.", icon="✅")

        except Exception as error:
            st.error(f"[error] pdf ingestion failed: {error}")

        finally:
            if temporary_file_path and os.path.exists(temporary_file_path):
                os.remove(temporary_file_path)


# ========================= Stream response =========================

if user_input:
    # Save title from the very first user message in this thread
    set_thread_title(st.session_state["thread_id"], user_input)

    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
        "run_name": "chat_trace",
    }

    with st.chat_message("assistant"):
        status_holder = {"box": None}

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"⚙ tool :: {tool_name}", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"⚙ tool :: {tool_name}",
                            state="running",
                            expanded=True,
                        )

                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

            # Detect HITL interrupt
            pending_interrupt = get_pending_interrupt(st.session_state["thread_id"])
            if pending_interrupt is not None:
                save_pending_interrupt(st.session_state["thread_id"], pending_interrupt)
                yield (
                    "\n\n`[ HITL ]` this action requires your approval. "
                    "Use **✓ approve** or **✗ reject** above."
                )

        ai_message = st.write_stream(ai_only_stream())

        if status_holder["box"] is not None:
            if get_pending_interrupt(st.session_state["thread_id"]) is not None:
                status_holder["box"].update(
                    label="⏸ awaiting human approval",
                    state="complete",
                    expanded=False
                )
            else:
                status_holder["box"].update(
                    label="✓ tool complete",
                    state="complete",
                    expanded=False
                )

    st.session_state["message_history"].append({
        "role": "assistant",
        "content": ai_message
    })

    if (
        st.session_state.get("pending_hitl") is not None
        and st.session_state["pending_hitl"].get("thread_id")
        == st.session_state["thread_id"]
    ):
        st.rerun()