request = "I'd like to have an argument, please."
# The input function gets an argument here (in this case, a request)
answer  = input(request+"\n"+"  ")
# ...and it returns an answer which is used for further processing.

if (len(answer) > 10):
    import webbrowser as wb
    spam = wb.open_new_tab('https://youtu.be/ohDB5gbtaEQ')
elif (len(answer) > 0):
    print("Excuse me?")
else:
    print("No argument for you!")

print("The end.")


    