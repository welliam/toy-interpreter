(define collatz
  (lambda (n)
    (if (= n 1)
        null
        (begin
          (define next (if (= (modulo n 2) 0) (/ n 2) (+ (* n 3) 1)))
          (cons n (collatz next))))))
