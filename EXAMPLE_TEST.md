═══════════════════════════════════════════════════════════════════════════════
EXAMPLE TEST - QA RAG APPLICATION
═══════════════════════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════════════════════
SAMPLE INPUT DOCUMENT
═══════════════════════════════════════════════════════════════════════════════

The Renaissance was a cultural and intellectual movement spanning roughly the 14th 
to 17th centuries, beginning in Italy and spreading to the rest of Europe. It 
marked the transition from the Medieval period to the Modern era.

During the Renaissance, humanism became a dominant philosophical movement. Humanists 
believed in the potential for individual achievement and emphasized classical learning 
from ancient Greece and Rome. They promoted the study of literature, history, and 
philosophy as a means to understand human nature and society better.

Art during the Renaissance underwent a dramatic transformation. Artists began using 
linear perspective, creating more realistic and proportional representations of human 
figures and landscapes. Famous artists like Leonardo da Vinci, Michelangelo, and 
Raphael created masterpieces that remain influential today. The invention of the 
printing press by Johannes Gutenberg around 1440 revolutionized the spread of knowledge, 
allowing books to be produced more quickly and affordably.

Scientific advancement accelerated during this period. Astronomers like Nicolaus 
Copernicus and Galileo Galilei challenged the geocentric model of the universe, 
proposing that the Earth revolved around the Sun. These discoveries laid the 
groundwork for the Scientific Revolution of the 17th century.

The Renaissance saw the rise of powerful city-states in Italy, particularly Venice, 
Florence, and Milan. These cities became centers of commerce, art, and learning. 
Florence, under the patronage of the Medici family, became especially influential 
in promoting Renaissance ideals and supporting artists and scholars.

═══════════════════════════════════════════════════════════════════════════════
TEST SCENARIO 1: DIRECT FACTUAL QUESTION
═══════════════════════════════════════════════════════════════════════════════

Question:
"What did Johannes Gutenberg invent?"

Expected Answer Format:
"Johannes Gutenberg invented the printing press around 1440, which revolutionized 
the spread of knowledge by allowing books to be produced more quickly and affordably."

✓ CORRECT: Answer is grounded in the document
✓ CORRECT: Provides specific date (1440)
✓ CORRECT: Explains the impact

═══════════════════════════════════════════════════════════════════════════════
TEST SCENARIO 2: DEFINITION QUESTION
═══════════════════════════════════════════════════════════════════════════════

Question:
"What was humanism during the Renaissance?"

Expected Answer Format:
"Humanism was a dominant philosophical movement during the Renaissance that believed 
in the potential for individual achievement and emphasized classical learning from 
ancient Greece and Rome. Humanists promoted the study of literature, history, and 
philosophy as a means to understand human nature and society better."

✓ CORRECT: Provides definition from context
✓ CORRECT: Includes key characteristics
✓ CORRECT: References classical learning aspect

═══════════════════════════════════════════════════════════════════════════════
TEST SCENARIO 3: COMPARISON QUESTION
═══════════════════════════════════════════════════════════════════════════════

Question:
"How did art change during the Renaissance?"

Expected Answer Format:
"During the Renaissance, art underwent dramatic transformation. Artists began using 
linear perspective, creating more realistic and proportional representations of human 
figures and landscapes. Famous artists like Leonardo da Vinci, Michelangelo, and 
Raphael created masterpieces during this time."

✓ CORRECT: Contrasts with earlier periods
✓ CORRECT: Mentions key techniques (linear perspective)
✓ CORRECT: Names significant artists

═══════════════════════════════════════════════════════════════════════════════
TEST SCENARIO 4: QUESTION NOT IN DOCUMENT
═══════════════════════════════════════════════════════════════════════════════

Question:
"What was the population of Renaissance Italy?"

Expected Answer Format:
"Answer not found in the provided context."

✓ CORRECT: Returns standard "not found" message
✓ CORRECT: Doesn't guess or infer
✓ CORRECT: Strict adherence to context-only answering

═══════════════════════════════════════════════════════════════════════════════
TEST SCENARIO 5: MULTI-PART QUESTION
═══════════════════════════════════════════════════════════════════════════════

Question:
"Who were some famous Renaissance artists and what is known about them?"

Expected Answer Format:
"Famous Renaissance artists included Leonardo da Vinci, Michelangelo, and Raphael. 
They created masterpieces that remain influential today. These artists were part of 
the dramatic transformation of art during the Renaissance, where artists began using 
linear perspective to create more realistic and proportional representations of human 
figures and landscapes."

✓ CORRECT: Lists multiple artists
✓ CORRECT: Provides available context about their work
✓ CORRECT: Connects to broader Renaissance art trends

═══════════════════════════════════════════════════════════════════════════════
MANUAL TESTING STEPS
═══════════════════════════════════════════════════════════════════════════════

1. START THE APPLICATION:
   python app.py
   Open browser: http://localhost:5000

2. UPLOAD THE DOCUMENT:
   - Copy the Sample Input Document above
   - Paste into the textarea
   - Click "Upload & Process Document"
   - Wait for success message (should show approximately 4-5 chunks)

3. TEST QUESTION 1:
   - Input: "What did Johannes Gutenberg invent?"
   - Click "Get Answer"
   - Verify answer mentions printing press and year 1440
   - Status: ✓ PASS if answer is grounded in document

4. TEST QUESTION 2:
   - Input: "What was humanism during the Renaissance?"
   - Click "Get Answer"
   - Verify answer defines humanism and mentions classical learning
   - Status: ✓ PASS if definition is accurate

5. TEST QUESTION 3:
   - Input: "How did art change during the Renaissance?"
   - Click "Get Answer"
   - Verify answer mentions perspective and famous artists
   - Status: ✓ PASS if changes are clearly described

6. TEST QUESTION 4:
   - Input: "What was the population of Renaissance Italy?"
   - Click "Get Answer"
   - Verify answer returns "Answer not found in the provided context"
   - Status: ✓ PASS if no information is guessed

7. TEST QUESTION 5:
   - Input: "Who were some famous Renaissance artists?"
   - Click "Get Answer"
   - Verify answer lists Leonardo, Michelangelo, and Raphael
   - Status: ✓ PASS if artists are correctly identified

═══════════════════════════════════════════════════════════════════════════════
ERROR HANDLING TEST CASES
═══════════════════════════════════════════════════════════════════════════════

Test Case: Empty Document Upload
  - Try uploading empty text
  - Expected: Error message "Empty text provided"
  - Status: ✓ PASS

Test Case: Question Before Document Upload
  - Try asking a question without uploading document
  - Expected: Error "No document loaded. Please upload a document first."
  - Status: ✓ PASS

Test Case: Empty Question
  - Upload document, then submit empty question
  - Expected: Error "Question cannot be empty"
  - Status: ✓ PASS

Test Case: Invalid File Type
  - Try uploading .docx or .csv file
  - Expected: Error "Unsupported file type"
  - Status: ✓ PASS

═══════════════════════════════════════════════════════════════════════════════
PERFORMANCE TEST
═══════════════════════════════════════════════════════════════════════════════

Metric                          Expected Behavior
─────────────────────────────────────────────────
Document Upload Time             < 3 seconds
Embedding Creation Time          < 2 seconds (for ~5 chunks)
Question Response Time           < 5 seconds (API call dependent)
Chunk Count Display              4-6 chunks for sample document
Spinner Animation                Smooth, visible during API calls
UI Responsiveness                No freezing during processing
Error Messages                   Clear and user-friendly

═══════════════════════════════════════════════════════════════════════════════
EXAMPLE API CURL COMMANDS
═══════════════════════════════════════════════════════════════════════════════

UPLOAD VIA TEXT:
curl -X POST http://localhost:5000/upload \
  -H "Content-Type: application/json" \
  -d '{"text": "The Renaissance was..."}'

Response:
{"status": "ready", "chunk_count": 5}

ASK QUESTION:
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What was humanism?"}'

Response:
{"answer": "Humanism was a dominant philosophical movement..."}

═══════════════════════════════════════════════════════════════════════════════
SUCCESS CRITERIA
═══════════════════════════════════════════════════════════════════════════════

✓ Application starts without errors
✓ Frontend UI loads with proper styling
✓ Document upload succeeds with chunk count display
✓ Questions are answered with relevant context
✓ Out-of-context questions return "not found" message
✓ All error cases handled gracefully
✓ Spinner displays during API calls
✓ Response formatting is clear and readable
✓ Application handles multiple uploads in single session
✓ No API errors for valid operations

═══════════════════════════════════════════════════════════════════════════════
