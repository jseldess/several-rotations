// Incomplete version of several_rotations.py in Go.

package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"time"
)

func main() {

	rand.Seed(time.Now().Unix())

	var source = flag.String("source", "source.txt", "source text file")
	var uniqueLines = flag.Bool("unique-lines", false, "use each unique line from the source file only once (default: false)")
	var newFileDir = flag.String("new-file-dir", "generated_files/", "path to the directory where the new file will be created")
	flag.Parse()

	// Read a file and store its lines as a slice of strings.
	data, err := ioutil.ReadFile(*source)
	if err != nil {
		panic(err)
	}
	lines := strings.Split(string(data), "\n")

	// Get the current timestamp.
	timestamp := strconv.FormatInt(time.Now().UTC().UnixNano(), 10)

	pace := [8]string{"", "", "", "", "\n", "\n\n", "\n\n\n", "\n\n\n\n"}

	if *uniqueLines == false {
		// Create a new file named with the current timestamp.
		new_file, err := os.Create(*newFileDir + timestamp + "_go.txt")
		if err != nil {
			panic(err)
		}

		for len(lines) > 0 {
			lineIndex := rand.Intn(len(lines))
			line := lines[lineIndex]
			new_file.WriteString(line + "\n")
			lines = append(lines[:lineIndex], lines[lineIndex+1:]...)
			paceIndex := rand.Intn(len(pace))
			next := pace[paceIndex]
			if len(next) > 0 {
				new_file.WriteString(next)
			}
		}

		fmt.Println("File " + timestamp + "_go.txt created")
		return

	} else {
		// Create a new file named with the current timestamp.
		new_file, err := os.Create(*newFileDir + timestamp + "_go_unique.txt")
		if err != nil {
			panic(err)
		}

		lines_seen := map[string]bool{}

		for len(lines) > 0 {
			lineIndex := rand.Intn(len(lines))
			line := lines[lineIndex]
			if lines_seen[line] {
				lines = append(lines[:lineIndex], lines[lineIndex+1:]...)
			} else {
				new_file.WriteString(line + "\n")
				lines = append(lines[:lineIndex], lines[lineIndex+1:]...)
				lines_seen[line] = true
				paceIndex := rand.Intn(len(pace))
				next := pace[paceIndex]
				if len(next) > 0 {
					new_file.WriteString(next)
				}
			}
		}
		fmt.Println("File " + timestamp + "_go_unique.txt created")
		return
	}
}
