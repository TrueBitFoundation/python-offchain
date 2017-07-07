(module
  (table 0 anyfunc)
  (memory $0 1)
  (export "memory" (memory $0))
  (export "main" (func $main))
  (func $main (param $0 i32) (param $1 i32) (result i32)
    (i32.const 17)
  )
)
