(define (problem pacman-01)
    (:domain pacman)
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
        ;; homeAt maps out the home area for pacman 
	    (homeAt loc-x0-y0)
	    (homeAt loc-x0-y1)
	    (homeAt loc-x0-y2)
	    (homeAt loc-x0-y3)
	    (homeAt loc-x0-y4)
	    (homeAt loc-x1-y0)
	    (homeAt loc-x1-y1)
	    (homeAt loc-x1-y2)
	    (homeAt loc-x1-y3)
	    (homeAt loc-x1-y4)
	    (homeAt loc-x2-y0)
	    (homeAt loc-x2-y1)
	    (homeAt loc-x2-y2)
	    (homeAt loc-x2-y3)
	    (homeAt loc-x2-y4)
	    (foodAt loc-x3-y3)
	    (foodAt loc-x4-y1)
	    (foodAt loc-x4-y2)
	    (pacmanAt loc-x4-y3)
	    (ghostAt loc-x4-y0)
	    (pelletAt loc-x2-y2)
    )
    
    (:goal
        (and 
	         (home)
        )
    )
)