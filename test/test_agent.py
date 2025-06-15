import unittest
from src.agent import Agent

class TestAgent(unittest.TestCase):
    def test_chat(self):
        """Test the Agent's chat functionality."""
        agent = Agent()
        prompts = [
            "What's the company TESLA stock symbol in New York exchange?",
            "Where is it located?",
            "Who is the CEO, do you like him or her?",
        ]
        for prompt in prompts:
            agent.chat(prompt)
            self.assertIsNotNone(agent.answer)
            self.assertIsInstance(agent.answer, str)  # Ensure the answer is a string
            print(f"Prompt: {prompt}\nAnswer: {agent.answer}\n")

if __name__ == "__main__":
    unittest.main()