TARGET = honorscontract

$(TARGET): $(TARGET).py
	cp ./$(TARGET).py gpt_info
	chmod +x gpt_info