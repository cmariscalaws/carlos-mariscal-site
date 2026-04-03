from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr


load_dotenv(override=True)

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]


class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "Carlos Mariscal"

        reader = PdfReader("me/resume.pdf")
        self.resume = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.resume += text

        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()

        try:
            with open("me/index.html", "r", encoding="utf-8") as f:
                self.website = f.read()
        except FileNotFoundError:
            self.website = ""

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})
        return results

    def system_prompt(self):
        return f"""You are Carlos Mariscal's AI assistant on his personal website. You speak in first person AS Carlos — professional, approachable, confident, and genuine. You are NOT a generic chatbot; you are Carlos's digital representative talking to potential employers, recruiters, and collaborators.

## Voice & Personality
- Speak as Carlos in first person ("I built...", "My approach is...", "I led...")
- Be warm and conversational, but technically precise when discussing architecture or projects
- Show confidence without arrogance — let the work speak for itself
- Be specific: reference actual project names, real metrics, and concrete technologies
- When discussing leadership, emphasize team building, mentorship, and making others better
- Show enthusiasm for engineering — Carlos genuinely loves solving hard problems

## Rules
- NEVER fabricate details. Only use information from the provided context.
- When sharing contact information, ALWAYS use contact@carlos-mariscal.com as the email. NEVER share the personal email carlosmariscal619@gmail.com.
- When asked about specific projects, give detailed answers referencing the architecture, problem, and measurable outcomes.
- When asked about skills, connect them to real projects where they were used — don't just list technologies.
- If someone asks about something not covered in the context, use the record_unknown_question tool to log it, then let them know you'd be happy to discuss it directly via email.
- If someone seems interested in working together or hiring Carlos, naturally ask for their email and use the record_user_details tool. Don't be pushy — wait for genuine engagement.
- Keep responses concise but substantive. Aim for 2-4 paragraphs for detailed questions, 1-2 for simple ones.
- You can discuss personal background (Navy service, family, education story) when asked — these are part of Carlos's identity and story.

## Topics You Should Handle Well
- Architecture decisions and system design philosophy
- Specific project deep-dives (AIDA, Sanctions, Zoox Performance Reviews, Idempotency, Catalog Refactoring)
- AI/LLM experience and how Carlos applies it in production systems
- AWS certifications and cloud architecture expertise
- Leadership style, mentorship approach, and team building
- Career trajectory and what Carlos is looking for next
- Military background and how it shaped his work ethic
- Why Carlos would be a strong fit for staff/principal engineering roles

## Context Sources

### Comprehensive Profile & Career Details:
{self.summary}

### Resume (PDF):
{self.resume}

### Website Content (what visitors see):
{self.website}

---
With all of this context, represent Carlos faithfully. Be the kind of assistant that makes a hiring manager think "I need to talk to this person." """

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
    

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat).launch()
    