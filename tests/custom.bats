load harness

@test "custom-1" {
  check 'x := 10 < 20 ? 1 : 0' '{x → 1}'
}

@test "custom-2" {
  check 'x := 10 ; y := x = 10 ? x * x : 0' '{x → 10, y → 100}'
}

@test "custom-3" {
  check 'x := -1 ; while 0 < x ? true : false do skip' '{x → -1}'
}

@test "custom-4" {
  check 'x := -1 ; while x < 10 ? true : false do x := x + 1' '{x → 10}'
}

@test "custom-5" {
  check 'x := 10 ; y := x < 12 ? 11 : 9 ; while 10 < x * y do { if y < x then x := x - 1 else y := y - 1 }' '{x → 3, y → 3}'
}

@test "custom-6" {
  check 'x := ¬ ( y - -3 = y * z ∨ n * y < 1 * 2 ) ? 1 : 0' '{x → 0}'
}
