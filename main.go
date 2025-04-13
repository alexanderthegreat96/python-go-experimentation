package main

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"os"
)

// setting up our struct
// for json decoding
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

	// we're expecting a base64 encoded json string so we simply
	dc, err := base64.RawStdEncoding.DecodeString(string(bytes))
	if err != nil {
		fmt.Fprintf(os.Stderr, "error base64 decoding input: %v\n", err)
		os.Exit(1)
	}

	// decode and map the decoded data to the struct
	if err := json.Unmarshal(dc, &input); err != nil {
		fmt.Fprintf(os.Stderr, "error decoding input: %v\n", err)
		os.Exit(1)
	}

	// use the struct to actually do something
	output := Output{
		Message: fmt.Sprintf("Hello, %s! You are %d years old.", input.Name, input.Age),
	}

	// return the json encoded output
	result, _ := json.Marshal(output)
	fmt.Println(string(result))
}
