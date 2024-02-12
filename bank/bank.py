#prompts for greeting, gives $0 for hello, $20 if begins witn an 'h', $100 otherwise
greeting = input("Greeting: ").lower().strip()
words = greeting.split()
text = words[0]
if text[0] == "h" and "hello" in text:
    print("$0")
elif text[0] == "h":
    print("$20")
else:
    print("$100")
