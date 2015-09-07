def tokenize(lisp):
    # add spaces after ( and before )
    # to get all the tokens
    slisp = lisp.strip().replace("(", "( ").replace(")", " )")
    return slisp.split()

def parse(tokens):
    def parse_internal(tokens, counter):
        parsed = []
        start_at = counter
        while counter < len(tokens):
            tok = tokens[counter]
            if tok == '(':
                # if we encounter a nesting,
                # call the function parse to get
                # AST for the nesting first
                res = parse_internal(tokens, counter + 1)
                # if its an error message, just pass it down the recursion stack
                if res[1] == -1:
                    return res

                nested_list = res[0]
                counter     = res[1]       # update the counter
                parsed.append(nested_list) # append the nested list
            elif tok == ')':
                return parsed, counter
            else:
                parsed.append(tok)
            counter += 1
        # we'll only reach here if we didn't encounter a correspoding ')'
        return ("Missing closing parenthesis for ( - token#%d" % (start_at,), -1)
    res = parse_internal(tokens, 1)
    if res[1] != -1 and res[1] < len(tokens) - 1:
        return "Extra closing parenthesis"
    else:
        return res[0]

def add_lisp(function_call_list):
        sumed = 0
        for i in range(1, len(function_call_list)):
                sumed += evaluate(function_call_list[i])
        return sumed

def evaluate(tokens):
        if isinstance(tokens, list):
                # it has special meaning 
                mapping = {
                        "+" : add_lisp,
                        "add": add_lisp,
                }
                return mapping[tokens[0]](tokens)
        return int(tokens)  

# (+ 3 (add 4 (add 5)) 6 7 8 9 10)
# ["+", 3, ["add", 4, ["add", 5]], 6, 7, 8, 9, 10]
# ["+", 3, 4, 5, 6, 7, 8, 9, 10]
# add(["+", 3, 4, 5, 6, 7, 8, 9, 10])


print evaluate(parse(tokenize("(+ 3 (add 4 (add 5)) 6 7 8 9 10)")))
