package main

import "fmt"

func main() {
	func1("duri", "suta")
	func4(3, 2)

}
func func1(person1, person2 string) {
	fmt.Println("Hello " + person1 + " aar " + person2)

}
func func4(a, b int) {
	fmt.Println(a + b)

}
