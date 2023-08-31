import os
import openai


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']
'''
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


'''

# function that takes in string argument as parameter
def get_completion(PROMPT, MaxToken=250, outputs=3):
	# using OpenAI's Completion module that helps execute
	# any tasks involving text
	response = openai.Completion.create(
		# model name used here is text-davinci-003
		# there are many other models available under the
		# umbrella of GPT-3
		model="text-davinci-003",
		# passing the user input
		prompt=PROMPT,
		# generated output can have "max_tokens" number of tokens
		max_tokens=MaxToken,
		# number of outputs generated in one call
		n=outputs
	)
	# creating a list to store all the outputs
	output = list()
	for k in response['choices']:
		output.append(k['text'].strip())
	return output


