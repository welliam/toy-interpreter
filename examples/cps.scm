(define cons& (lambda (a b k) (k (cons a b))))
(define head& (lambda (p k) (k (head p))))
(define tail& (lambda (p k) (k (tail p))))
(define =& (lambda (a b k) (k (= a b))))

(define if&
  (lambda (exp truek falsek)
    ((if exp truek falsek))))

(define reverse&
  (lambda (t k)
    (reverse-help& t null k)))

(define reverse-help&
  (lambda (t res k)
    (=& t null
        (lambda (t-null?)
          (if& t-null?
               (lambda ()
                 (k res))
               (lambda ()
                 (head& t
                   (lambda (t-head)
                     (tail& t
                       (lambda (t-tail)
                         (cons& t-head res
                           (lambda (new-res)
                             (reverse-help& t-tail new-res k)))))))))))))

(define length
  (lambda (t)
    (if (= t null)
        0
        (+ 1 (length (tail t))))))

(reverse& (cons 1 (cons 2 (cons 3 null))) print)
