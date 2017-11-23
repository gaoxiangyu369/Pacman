(define (problem ghost-01)
    (:domain ghost)
    (:objects 
    ;; position maps the whole maze
	    loc-x0-y0
	    loc-x0-y1
	    loc-x0-y2
	    loc-x0-y3
	    loc-x0-y4
	    loc-x1-y0
	    loc-x1-y1
	    loc-x1-y2
	    loc-x1-y3
	    loc-x1-y4
	    loc-x2-y0
	    loc-x2-y1
	    loc-x2-y2
	    loc-x2-y3
	    loc-x2-y4
	    loc-x3-y0
	    loc-x3-y1
	    loc-x3-y2
	    loc-x3-y3
	    loc-x3-y4
	    loc-x4-y0
	    loc-x4-y1
	    loc-x4-y2
	    loc-x4-y3
	    loc-x4-y4
    - position 
    )
    
    (:init
    ;; adjacent outlines the available paths
        (adjacent loc-x0-y0 loc-x1-y0)
        (adjacent loc-x0-y0 loc-x0-y1)
        (adjacent loc-x0-y1 loc-x0-y0)
        (adjacent loc-x0-y1 loc-x0-y2)
        (adjacent loc-x0-y2 loc-x0-y1)
        (adjacent loc-x0-y2 loc-x0-y3)
        (adjacent loc-x0-y3 loc-x0-y2)
        (adjacent loc-x0-y3 loc-x0-y4)
        (adjacent loc-x0-y3 loc-x1-y3)
        (adjacent loc-x1-y3 loc-x0-y3)
        (adjacent loc-x1-y3 loc-x2-y3)
        (adjacent loc-x1-y0 loc-x0-y0)
        (adjacent loc-x1-y0 loc-x2-y0)
        (adjacent loc-x2-y0 loc-x1-y0)
        (adjacent loc-x2-y0 loc-x2-y1)
        (adjacent loc-x2-y0 loc-x3-y0)
        (adjacent loc-x2-y1 loc-x2-y0)
        (adjacent loc-x2-y1 loc-x2-y2)
        (adjacent loc-x3-y0 loc-x2-y0)
        (adjacent loc-x3-y0 loc-x4-y0)
        (adjacent loc-x4-y0 loc-x3-y0)
        (adjacent loc-x4-y0 loc-x4-y1)
        (adjacent loc-x4-y1 loc-x4-y0)
        (adjacent loc-x4-y1 loc-x4-y2)
        (adjacent loc-x4-y2 loc-x4-y1)
        (adjacent loc-x4-y2 loc-x4-y3)
        (adjacent loc-x4-y3 loc-x4-y2)
        (adjacent loc-x4-y3 loc-x3-y3)
        (adjacent loc-x3-y3 loc-x4-y3)
        (adjacent loc-x3-y3 loc-x2-y3)
        (adjacent loc-x2-y2 loc-x2-y3)
        (adjacent loc-x2-y2 loc-x2-y1)
        (adjacent loc-x2-y3 loc-x2-y2)
        (adjacent loc-x2-y3 loc-x1-y3)
        (adjacent loc-x2-y3 loc-x3-y3)
        (adjacent loc-x2-y3 loc-x2-y4)
        (adjacent loc-x2-y4 loc-x2-y3)
        ;; the following states the pacman, ghost, pellet and food position
	    (ghostAt loc-x2-y0)
	    (pacmanAt loc-x0-y2)
	    (pacmanAt loc-x4-y2)
    )
    
    (:goal
        (and (not (pacmanAt loc-x0-y2))
             (not (pacmanAt loc-x4-y2))
        )
    )
)