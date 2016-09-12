(define collatz
  (lambda (n)
    (if (= n 1)
        null
        (begin
          (define next (if (% n 2) (+ (* n 3) 1) (/ n 2)))
          (cons n (collatz next))))))
