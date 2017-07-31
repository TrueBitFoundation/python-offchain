(module
  (type $FUNCSIG$ii (func (param i32) (result i32)))
  (type $FUNCSIG$iii (func (param i32 i32) (result i32)))
  (type $FUNCSIG$vi (func (param i32)))
  (type $FUNCSIG$i (func (result i32)))
  (type $FUNCSIG$iiiii (func (param i32 i32 i32 i32) (result i32)))
  (type $FUNCSIG$iiii (func (param i32 i32 i32) (result i32)))
  (type $FUNCSIG$v (func))
  (import "env" "chdir" (func $chdir (param i32) (result i32)))
  (import "env" "close" (func $close (param i32) (result i32)))
  (import "env" "ctime" (func $ctime (param i32) (result i32)))
  (import "env" "exit" (func $exit (param i32)))
  (import "env" "fclose" (func $fclose (param i32) (result i32)))
  (import "env" "fopen" (func $fopen (param i32 i32) (result i32)))
  (import "env" "fork" (func $fork (result i32)))
  (import "env" "fprintf" (func $fprintf (param i32 i32 i32) (result i32)))
  (import "env" "fputs" (func $fputs (param i32 i32) (result i32)))
  (import "env" "fwrite" (func $fwrite (param i32 i32 i32 i32) (result i32)))
  (import "env" "mutator_server" (func $mutator_server (param i32) (result i32)))
  (import "env" "setsid" (func $setsid (result i32)))
  (import "env" "signal" (func $signal (param i32 i32) (result i32)))
  (import "env" "time" (func $time (param i32) (result i32)))
  (import "env" "umask" (func $umask (param i32) (result i32)))
  (table 3 3 anyfunc)
  (elem (i32.const 0) $__wasm_nullptr $sigint_callback_handler $sigterm_callback_handler)
  (memory $0 1)
  (data (i32.const 16) "mutatord-log\00")
  (data (i32.const 32) "w\00")
  (data (i32.const 48) "daemon started on \00")
  (data (i32.const 80) "child forked on \00")
  (data (i32.const 112) "%s%d%s\00")
  (data (i32.const 128) "successfully got a pid:\00")
  (data (i32.const 160) "\n\00")
  (data (i32.const 176) "set umask to 0.\n\00")
  (data (i32.const 208) "failed to get an sid.\n\00")
  (data (i32.const 240) "got an sid:\00")
  (data (i32.const 256) "/\00")
  (data (i32.const 272) "failed to change to root dir.\n\00")
  (data (i32.const 304) "changed to root dir.\n\00")
  (data (i32.const 336) "closed standard file descriptors..\n\00")
  (data (i32.const 384) "running server...\n\00")
  (data (i32.const 416) "server terminated with exit code \00")
  (data (i32.const 464) "closing down server\n\00")
  (export "memory" (memory $0))
  (export "time_n_date" (func $time_n_date))
  (export "sigint_callback_handler" (func $sigint_callback_handler))
  (export "sigterm_callback_handler" (func $sigterm_callback_handler))
  (export "main" (func $main))
  (func $time_n_date (param $0 i32)
    (local $1 i32)
    (i32.store offset=4
      (i32.const 0)
      (tee_local $1
        (i32.sub
          (i32.load offset=4
            (i32.const 0)
          )
          (i32.const 16)
        )
      )
    )
    (i32.store offset=12
      (get_local $1)
      (call $time
        (i32.const 0)
      )
    )
    (drop
      (call $fputs
        (call $ctime
          (i32.add
            (get_local $1)
            (i32.const 12)
          )
        )
        (get_local $0)
      )
    )
    (i32.store offset=4
      (i32.const 0)
      (i32.add
        (get_local $1)
        (i32.const 16)
      )
    )
  )
  (func $sigint_callback_handler (type $FUNCSIG$vi) (param $0 i32)
    (call $exit
      (get_local $0)
    )
    (unreachable)
  )
  (func $sigterm_callback_handler (type $FUNCSIG$vi) (param $0 i32)
    (call $exit
      (get_local $0)
    )
    (unreachable)
  )
  (func $main (result i32)
    (local $0 i32)
    (local $1 i32)
    (local $2 i32)
    (i32.store offset=4
      (i32.const 0)
      (tee_local $2
        (i32.sub
          (i32.load offset=4
            (i32.const 0)
          )
          (i32.const 48)
        )
      )
    )
    (drop
      (call $signal
        (i32.const 2)
        (i32.const 1)
      )
    )
    (drop
      (call $signal
        (i32.const 15)
        (i32.const 2)
      )
    )
    (drop
      (call $fwrite
        (i32.const 48)
        (i32.const 18)
        (i32.const 1)
        (tee_local $0
          (call $fopen
            (i32.const 16)
            (i32.const 32)
          )
        )
      )
    )
    (i32.store offset=44
      (get_local $2)
      (call $time
        (i32.const 0)
      )
    )
    (drop
      (call $fputs
        (call $ctime
          (i32.add
            (get_local $2)
            (i32.const 44)
          )
        )
        (get_local $0)
      )
    )
    (set_local $1
      (call $fork)
    )
    (drop
      (call $fwrite
        (i32.const 80)
        (i32.const 16)
        (i32.const 1)
        (get_local $0)
      )
    )
    (i32.store offset=44
      (get_local $2)
      (call $time
        (i32.const 0)
      )
    )
    (drop
      (call $fputs
        (call $ctime
          (i32.add
            (get_local $2)
            (i32.const 44)
          )
        )
        (get_local $0)
      )
    )
    (block $label$0
      (block $label$1
        (block $label$2
          (block $label$3
            (br_if $label$3
              (i32.le_s
                (get_local $1)
                (i32.const -1)
              )
            )
            (br_if $label$2
              (get_local $1)
            )
            (drop
              (call $umask
                (i32.const 0)
              )
            )
            (drop
              (call $fwrite
                (i32.const 176)
                (i32.const 16)
                (i32.const 1)
                (get_local $0)
              )
            )
            (br_if $label$1
              (i32.le_s
                (tee_local $1
                  (call $setsid)
                )
                (i32.const -1)
              )
            )
            (i32.store offset=24
              (get_local $2)
              (i32.const 160)
            )
            (i32.store offset=20
              (get_local $2)
              (get_local $1)
            )
            (i32.store offset=16
              (get_local $2)
              (i32.const 240)
            )
            (drop
              (call $fprintf
                (get_local $0)
                (i32.const 112)
                (i32.add
                  (get_local $2)
                  (i32.const 16)
                )
              )
            )
            (br_if $label$0
              (i32.le_s
                (call $chdir
                  (i32.const 256)
                )
                (i32.const -1)
              )
            )
            (drop
              (call $fwrite
                (i32.const 304)
                (i32.const 21)
                (i32.const 1)
                (get_local $0)
              )
            )
            (drop
              (call $close
                (i32.const 0)
              )
            )
            (drop
              (call $close
                (i32.const 1)
              )
            )
            (drop
              (call $close
                (i32.const 2)
              )
            )
            (drop
              (call $fwrite
                (i32.const 336)
                (i32.const 35)
                (i32.const 1)
                (get_local $0)
              )
            )
            (drop
              (call $fwrite
                (i32.const 384)
                (i32.const 18)
                (i32.const 1)
                (get_local $0)
              )
            )
            (set_local $1
              (call $mutator_server
                (get_local $0)
              )
            )
            (i32.store offset=8
              (get_local $2)
              (i32.const 160)
            )
            (i32.store offset=4
              (get_local $2)
              (get_local $1)
            )
            (i32.store
              (get_local $2)
              (i32.const 416)
            )
            (drop
              (call $fprintf
                (get_local $0)
                (i32.const 112)
                (get_local $2)
              )
            )
            (drop
              (call $fwrite
                (i32.const 464)
                (i32.const 20)
                (i32.const 1)
                (get_local $0)
              )
            )
            (drop
              (call $fclose
                (get_local $0)
              )
            )
            (i32.store offset=4
              (i32.const 0)
              (i32.add
                (get_local $2)
                (i32.const 48)
              )
            )
            (return
              (get_local $1)
            )
          )
          (call $exit
            (i32.const 1)
          )
          (unreachable)
        )
        (i32.store offset=40
          (get_local $2)
          (i32.const 160)
        )
        (i32.store offset=36
          (get_local $2)
          (get_local $1)
        )
        (i32.store offset=32
          (get_local $2)
          (i32.const 128)
        )
        (drop
          (call $fprintf
            (get_local $0)
            (i32.const 112)
            (i32.add
              (get_local $2)
              (i32.const 32)
            )
          )
        )
        (call $exit
          (i32.const 0)
        )
        (unreachable)
      )
      (drop
        (call $fwrite
          (i32.const 208)
          (i32.const 22)
          (i32.const 1)
          (get_local $0)
        )
      )
      (call $exit
        (i32.const 1)
      )
      (unreachable)
    )
    (drop
      (call $fwrite
        (i32.const 272)
        (i32.const 30)
        (i32.const 1)
        (get_local $0)
      )
    )
    (call $exit
      (i32.const 1)
    )
    (unreachable)
  )
  (func $__wasm_nullptr (type $FUNCSIG$v)
    (unreachable)
  )
)
