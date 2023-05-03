import os, glob, config, openai, traceback
# brew/apt install opencc
# pip3 install opencc-python-reimplemented
from opencc import OpenCC

"""
A menu plugin used with Unique Bible App
"""

def convertToTraditionalChinese(text):
    cc = OpenCC('s2t')
    return cc.convert(text)

def loadResponses(userInput):
    #messages
    messages = [
        {"role": "system", "content" : "You’re a kind helpful translator"}
    ]
    messages.append({"role": "assistant", "content": "Translate the following content into traditional Chinese:"})
    messages.append({"role": "user", "content": userInput})

    # responses
    chat_response = ""
    errors = ""
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=2048,
            temperature=1.0,
            n=1,
        )
        chat_response = completion.choices[0].message.content
    # error codes: https://platform.openai.com/docs/guides/error-codes/python-library-error-types
    except openai.error.APIError as e:
        #Handle API error here, e.g. retry or log
        errors = f"API Errors! OpenAI API returned an API Error: {e}"
    except openai.error.APIConnectionError as e:
        #Handle connection error here
        errors = f"Failed to connect to OpenAI API: {e}"
    except openai.error.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        errors = f"OpenAI API request exceeded rate limit: {e}"
    except:
        errors = traceback.format_exc()
        errors = f"API Errors! {errors}"
    if errors:
        return errors
    return chat_response

openai.api_key = os.environ["OPENAI_API_KEY"] = config.openaiApiKey
openai.organization = config.openaiApiOrganization
cwd = os.getcwd()

for i in os.listdir(cwd):
    if os.path.isdir(i) and not i[0] in ("_", ".") and not i == "00_Introduction":
        for ii in glob.glob(f"{cwd}/{i}/*.md"):
            print(f"Translating '{ii}' ...")
            with open(ii, "r", encoding="utf-8") as fileObj:
                text = fileObj.read()
            
            try:
                translatedText = loadResponses(text)
            except:
                translatedText = ""
                print(f"Failed to translate file '{ii}'!")
            
            if translatedText:
                translatedText = convertToTraditionalChinese(translatedText)
                with open(ii, "w", encoding="utf-8") as fileObj:
                    fileObj.write(translatedText)

print('Done!')