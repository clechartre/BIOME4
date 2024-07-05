FC = $(CONDA_PREFIX)/bin/gfortran
FCFLAGS  = -v  # Verbose output

# Use the paths from your Conda environment
# Replace <conda_env_path> with the actual path from nf-config --all
netcdf = $(CONDA_PREFIX)

# should not need to modify anything below this line

#---------------------------------------------

NC_LIB = $(netcdf)/lib
NC_INC = $(netcdf)/include

CPPFLAGS = -I$(NC_INC)
LDFLAGS  = -L$(NC_LIB)
LIBS     = -L/opt/homebrew/Caskroom/miniforge/base/envs/biome4 -lnetcdff -lcurl

#---------------------------------------------

OBJS = parametersmod.o  \
       netcdfmod.o      \
       coordsmod.o      \
       biome4.o         \
       biome4driver.o

#---------------------------------------------

.SUFFIXES: .o .f90 .f .mod

%.o : %.c
	$(CC) $(CFLAGS) -c -o $(*F).o $(CPPFLAGS) $<

%.o : %.f
	$(FC) $(FCFLAGS) -c -o $(*F).o $(CPPFLAGS) $<

%.o : %.f90
	$(FC) $(FCFLAGS) -c -o $(*F).o $(CPPFLAGS) $<

all::	biome4

biome4: $(OBJS)
	$(FC) $(FCFLAGS) -o biome4 $(OBJS) $(LDFLAGS) $(LIBS)

clean::	
	-rm *.o *.mod

# Debugging print statements
debug::
	@echo "NetCDF Library Path: $(NC_LIB)"
	@echo "NetCDF Include Path: $(NC_INC)"
	@echo "CPPFLAGS: $(CPPFLAGS)"
	@echo "LDFLAGS: $(LDFLAGS)"
	@echo "LIBS: $(LIBS)"

# Check for netcdf.mod file
check::
	@echo "Checking for netcdf.mod in $(NC_INC)"
	@if [ -f "$(NC_INC)/netcdf.mod" ]; then echo "netcdf.mod found"; else echo "netcdf.mod not found"; fi
