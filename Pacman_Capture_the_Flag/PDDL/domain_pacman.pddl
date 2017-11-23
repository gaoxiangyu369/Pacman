(define (domain pacman)
    (:requirements :typing :conditional-effects)
    (:types        position)
    (:predicates (pacmanAt ?x - position);; pacman's position
	             (foodAt ?x - position) ;; food position
	             (pelletAt ?x - position) ;; pellet position
	             (homeAt ?x - position) ;; the home area
	             (ghostAt ?x - position) ;; ghost position
	             (adjacent ?x ?y - position) ;; available path
	             (powered) ;; powered state 
	             (home) ;; home state
    )
    
    ;; the pacman move around to try to finish to goal
     (:action move
        :parameters (?from ?to - position)
        :precondition (and (pacmanAt ?from) 
                           (adjacent ?from ?to)
                           (not (ghostAt ?to))
                      )
        :effect (and (pacmanAt ?to)
                     (not (pacmanAt ?from))
                     (not (foodAt ?to))
                     (when (pelletAt ?to) (powered))
                     (not (pelletAt ?to))
                )
    )
	
	;; when the goal changes to home, the back action applies
	(:action back
        :parameters (?from ?to - position)
        :precondition (and (pacmanAt ?from) 
                           (adjacent ?from ?to)
                           (not (ghostAt ?to))
                           (not (home))
                      )
        :effect (and (pacmanAt ?to)
                     (not (pacmanAt ?from))
                     (not (foodAt ?to))
                     (when (pelletAt ?to) (powered))
                     (when (homeAt ?to) (home))
                     (not (pelletAt ?to))
                )
    )
	
	;; applies when the pacman is powered and the goal is to eat ghoat
    (:action eatGhost
        :parameters (?from ?to - position)
        :precondition (and (pacmanAt ?from) 
                           (adjacent ?from ?to)
                           (powered)
                           (ghostAt ?to)
                      )
        :effect (and (not (ghostAt ?to))
                     (not (pacmanAt ?from))
                     (pacmanAt ?to)
                )
    )
)