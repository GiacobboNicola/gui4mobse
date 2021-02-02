TARGET: mobse.a

MOBSE_PATH = mobse/src
CMPLR = gfortran
FFLAGS = -O2 -fcheck=all

VPATH = $(MOBSE_PATH)

MAIN = mobseGUI.f
SRC := $(shell find $(MOBSE_PATH) -type f  \( -iname '*.f' ! -iname 'mo[sb]se.f' \) )
OBJ := $(SRC:.f=.o)

mobse.a: $(OBJ)
	ar rcs $@ $^

mobseGUI: mobse.a mobse/input/const_mobse.h mobse/input/zdata.h
	$(CMPLR) $(FFLAGS) $(MAIN) $< -o mobseGUI.x -L./ 

clean:
	rm -f $(MOBSE_PATH)/*.o *.o mobseGUI.x mobse.a
