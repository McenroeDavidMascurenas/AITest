# Prompt Engineering Template Book

A comprehensive collection of reusable prompt patterns for AI tools like ChatGPT, Claude, Gemini, etc.

---

## A. Basic Prompt Templates

### 1. General Inquiry
**Template:** Ask a general question about a topic.  
**Example:**  
> What is AGI in simple words?

---

### 2. Summarization
**Template:** Summarize content with specific rules (length, style, format).  
**Example:**  
> Summarize this article in exactly 4 bullet points.

---

### 3. Paraphrasing
**Template:** Rewrite text without changing the core meaning.  
**Example:**  
> Rewrite this sentence in simpler English: “Artificial intelligence will transform global industries.”

---

### 4. Definition Request
**Template:** Ask for a concise explanation or definition.  
**Example:**  
> Define “vector embeddings” in one clear sentence.

---

### 5. Comparison
**Template:** Compare items based on criteria.  
**Example:**  
> Compare GPT-4 and Gemini 2.0 in terms of accuracy, speed, and cost.

---

## B. Persona-Based Prompt Templates

### 6. Role + Explanation
**Template:**  
> You are a [role]. Explain [concept] to [audience].

**Example:**  
> You are a lawyer. Explain “intellectual property” to a college student.

---

### 7. Style Mimicry
**Template:**  
> Write in the style of [author/person] about [topic].

**Example:**  
> Explain friendship in the style of Pablo Neruda.

---

### 8. Professional Writing
**Template:**  
> You are a [job title]. Write a [document type] about [topic].

**Example:**  
> You are a project manager. Write a risk log entry for an IT migration project.

---

## C. Few-Shot Prompt Templates

### 9. Classification Template
**Template:** Provide labeled examples, then ask for a label for a new sentence.

```
“Awesome product!” → Positive  
“This is terrible.” → Negative  
“It’s okay, nothing special.” → Neutral  

Classify: “The service was slow but the food was nice.”
```

---

### 10. Translation Template
**Template:** Show some translation mappings, then ask for a new translation.

```
Hello – வணக்கம்  
Good morning – காலை வணக்கம்  

Translate: “Have a great day.”
```

---

### 11. Question Answering Template
**Template:** Provide Q&A pairs, then let the model answer the next one.

```
Q: Who discovered gravity?  
A: Isaac Newton  

Q: What is the capital of Japan?  
A: Tokyo  

Q: What is the chemical symbol for water?
```

---

## D. Chain-of-Thought (CoT) Templates

### 12. Step-by-Step Reasoning
**Template:**  
> Think step by step and explain your reasoning.

**Example:**  
> Think step by step. How can someone start a YouTube channel from zero?

---

### 13. Math Problem Solving
**Template:**  
> Solve this math problem step by step and show all working.

**Example:**  
> Solve step by step: (45 ÷ 3) + 12 × 2

---

### 14. Logical Puzzle
**Template:**  
> Explain step by step how to solve this logical puzzle.

**Example:**  
> Explain step by step how to solve the classic river crossing puzzle with the fox, goat, and cabbage.

---

## E. Instruction Tuning / Format Control

### 15. Output Formatting
**Template:**  
> Answer in this format: [bullets / numbered list / JSON / table].

**Example:**  
> List 5 benefits of AI in bullet points only.

---

### 16. Table Generation
**Template:**  
> Create a table comparing [items] by [criteria].

**Example:**  
> Create a table comparing iPhone 15, Pixel 8, and Samsung S24 by battery, camera, and display.

---

### 17. Email Writing
**Template:**  
> Write a [tone] email to [recipient] about [topic].

**Example:**  
> Write a polite email requesting a project deadline extension.

---

## F. Contextual Prompts

### 18. Tailored Explanation
**Template:**  
> Explain [topic] to [age group / background] in simple terms.

**Example:**  
> Explain blockchain to a 12-year-old.

---

### 19. Industry-Specific Context
**Template:**  
> As a [expert role], explain how [topic] impacts [industry].

**Example:**  
> As a banker, explain how AI impacts credit risk assessment.

---

## G. Creative Writing Prompts

### 20. Story Writing
**Template:**  
> Write a story about [character] who [goal] but faces [obstacle].

**Example:**  
> Write a story about a robot who wants to become a painter but struggles to understand human emotions.

---

### 21. Poem Writing
**Template:**  
> Write a [style] poem about [theme].

**Example:**  
> Write a short poem about hope in a classical Tamil style.

---

### 22. Dialogue Writing
**Template:**  
> Write a realistic dialogue between [Person A] and [Person B] about [topic].

**Example:**  
> Write a conversation between two friends deciding which city to move to for work.

---

## H. Code & Technical Prompts

### 23. Code Generation
**Template:**  
> Write a [language] function that [does something].

**Example:**  
> Write a Python function that checks if a number is prime.

---

### 24. Debugging Help
**Template:**  
> Here is some code. Find and fix the errors.

**Example:**  
> Fix this code:  
> ```python
> for i in range(5)
>     print(i)
> ```

---

### 25. API Documentation
**Template:**  
> Explain how to use the [API name] with an example request and response.

**Example:**  
> Explain how to call the OpenWeather API with a sample GET request and JSON response.

---

## I. Marketing & Business Prompts

### 26. Ad Copywriting
**Template:**  
> Write a compelling ad for [product/service] targeting [audience].

**Example:**  
> Write a 2-line Instagram ad for a new fitness app targeting young professionals.

---

### 27. Product Description
**Template:**  
> Write a persuasive product description for [product name].

**Example:**  
> Write a persuasive description for a smart water bottle that tracks hydration levels.

---

### 28. Social Media Post
**Template:**  
> Create a social media post promoting [event/product/idea] in a [tone].

**Example:**  
> Write a friendly LinkedIn post announcing the launch of our new AI automation tool.

---

## J. Customer Support & Service Prompts

### 29. Response to Complaint
**Template:**  
> Respond professionally to this customer complaint: [complaint].

**Example:**  
> Respond to a customer who says their parcel arrived damaged and late.

---

### 30. FAQ Generator
**Template:**  
> Generate [number] common FAQs and answers for [topic/product].

**Example:**  
> Generate 5 FAQs and answers for an online coding bootcamp.

---

## K. Education & Tutoring Prompts

### 31. Lesson Plan Creation
**Template:**  
> Create a step-by-step lesson plan to teach [topic] to [audience].

**Example:**  
> Create a 30-minute lesson plan to teach fractions to 6th grade students.

---

### 32. Quiz Generation
**Template:**  
> Generate a [number]-question quiz about [topic] with answers.

**Example:**  
> Generate a 5-question quiz on Python basics with answers.

---

### 33. Homework Help
**Template:**  
> Explain how to solve this [subject] problem: [question].

**Example:**  
> Explain how to solve: A car travels 150 km at a constant speed of 75 km/h. How much time does it take?

---

## L. Advanced Framework-Based Templates

### 34. ReAct Framework
**Structure:**  
- Thought: model thinks about what to do next  
- Action: model takes an action  
- Observation: result of the action  
- Answer: final answer

**Example:**
```
Thought: I need to find the quickest way to get to the office.
Action: Check Google Maps for current traffic.
Observation: Route A is 20 minutes, Route B is 35 minutes.
Answer: Take Route A to reach the office faster.
```

---

### 35. Tree of Thoughts (ToT)
**Template:**  
> Generate 3 possible solutions to [problem]. Evaluate each and choose the best one.

**Example:**  
> Generate three ways to learn AI (YouTube, self-study, online course), evaluate pros and cons, and recommend the best for a working professional.

---

### 36. Self-Consistency Prompting
**Template:**  
> Solve this question in 3 different ways and pick the most consistent answer.

**Example:**  
> What is the best strategy for long-term investing? Provide three approaches, then choose the most reliable.

---

## M. Prompt Optimization & Evaluation

### 37. Prompt Refinement
**Template:**  
> Improve this prompt: “[original prompt]”. Make it clearer, more specific, and structured.

**Example:**  
> Improve this prompt: “Tell me about marketing.”

---

### 38. Prompt Grading Rubric
**Template:**  
> Rate this prompt or output on a scale of 1–5 for:
> - Relevance  
> - Accuracy  
> - Clarity  
> - Fluency  
> - Creativity  
> Give a final score and brief feedback.

---

### 39. Prompt Iteration Challenge
**Template:**  
> Take this weak prompt: “[prompt]”. Rewrite it 3 times to improve clarity and effectiveness.

**Example:**  
> Rewrite this prompt 3 times: “Tell me some good stocks.”

---

## N. Real-World Application Prompts

### 40. Job Posting Creation
**Template:**  
> Write a job posting for [position] at [company]. Include responsibilities, requirements, and benefits.

**Example:**  
> Write a job posting for a Senior Data Analyst at Apple.

---

### 41. Resume Summary Builder
**Template:**  
> Create a professional resume summary based on these details: [experience, skills, achievements].

**Example:**  
> Create a 3-line summary for a software engineer with 5 years of experience in Python and cloud computing.

---

### 42. Business Proposal
**Template:**  
> Write a proposal for [project idea] to [client/investor]. Include objectives, methodology, and benefits.

**Example:**  
> Write a proposal to implement AI chatbots in a hospital for patient support.

---

## O. Miscellaneous Useful Templates

### 43. Opinion Writing
**Template:**  
> Write an opinion piece on [topic]. Use persuasive arguments and examples.

**Example:**  
> Write an opinion piece on “Will AI replace traditional exams?”

---

### 44. Debate Preparation
**Template:**  
> Prepare arguments for both sides of the debate: “[debate topic]”.

**Example:**  
> Prepare arguments for and against banning fireworks in cities.

---

### 45. Travel Planning
**Template:**  
> Plan a [number]-day trip to [destination] for [type of traveler]. Include activities, budget, and tips.

**Example:**  
> Plan a 5-day trip to Singapore for a family with kids.

---

### 46. Book/Movie Review
**Template:**  
> Write a review of [book/movie]. Include summary, strengths, weaknesses, and recommendation.

**Example:**  
> Write a detailed review of the movie “Interstellar.”

---

### 47. Personal Development
**Template:**  
> Give me actionable advice on how to [goal], including daily habits and mindset shifts.

**Example:**  
> Give me a daily routine to improve focus and productivity.

---

## P. Prompt Chaining Examples

### 48. Multi-step Research Task
**Template:**  
Step 1: [Research task]  
Step 2: [Synthesis/solution task]

**Example:**  
Step 1: List the top 5 causes of burnout.  
Step 2: Suggest a practical solution for each cause.

---

### 49. Idea to Execution
**Template:**  
> List [number] ideas for [theme], evaluate them using [criteria], and pick the best one.

**Example:**  
> List 5 small-scale digital business ideas, evaluate based on cost, scalability, and profit potential, and choose the best for 2025.

---

## Q. Prompt Template Generator

### 50. Universal Prompt Builder

**Formula:**  
> [Role] + [Task] + [Context] + [Example] + [Format]

**Example:**  
> Role: You are an excellent story writer for children.  
> Task: Create a bedtime story.  
> Context: Children under age 10; simple language.  
> Example: Fictional animal-based stories.  
> Format: Within 200 words, with short paragraphs.

---
