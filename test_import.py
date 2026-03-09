import traceback
try:
    import agents.voice_agent.voice_agent
    print("Success")
except Exception as e:
    with open("error_native.log", "w") as f:
        traceback.print_exc(file=f)
