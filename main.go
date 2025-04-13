package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
)

type Input struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
}

type Output struct {
	Message string `json:"message"`
}

func main() {
	var input Input
	bytes, err := io.ReadAll(os.Stdin)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error reading stdin: %v\n", err)
		os.Exit(1)
	}

	if err := json.Unmarshal(bytes, &input); err != nil {
		fmt.Fprintf(os.Stderr, "error decoding input: %v\n", err)
		os.Exit(1)
	}

	output := Output{
		Message: fmt.Sprintf("Hello, %s! You are %d years old.", input.Name, input.Age),
	}

	result, _ := json.Marshal(output)
	fmt.Println(string(result))
}
