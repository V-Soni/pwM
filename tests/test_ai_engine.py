import pytest
import os
from unittest.mock import patch, MagicMock

# Set a dummy API key for testing if not set
os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY", "dummy_key")

from ai_engine import analyze_mcq_results, generate_insights

@pytest.mark.asyncio
@patch('ai_engine.client.chat.completions.create')
async def test_analyze_mcq_results_stressed(mock_create):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Oh beta, why are you so stressed?"
    mock_create.return_value = mock_response

    answers = ["panicking", "didn't sleep", "forgot to eat"]
    mood, msg = await analyze_mcq_results(answers)
    
    assert mood == "Stressed"
    assert msg == "Oh beta, why are you so stressed?"

@pytest.mark.asyncio
@patch('ai_engine.client.chat.completions.create')
async def test_analyze_mcq_results_optimistic(mock_create):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "That's my child!"
    mock_create.return_value = mock_response

    answers = ["ready to go", "productive"]
    mood, msg = await analyze_mcq_results(answers)
    
    assert mood == "Optimistic"

@pytest.mark.asyncio
@patch('ai_engine.client.chat.completions.create')
async def test_generate_insights_fallback(mock_create):
    # Mocking a response that isn't valid JSON
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "I couldn't analyze this."
    mock_create.return_value = mock_response

    history = [{"role": "user", "content": "hello"}]
    result = await generate_insights(history)
    
    assert result["wellness_score"] == 5
    assert "Analysis could not be completed" in result["hidden_triggers"]
