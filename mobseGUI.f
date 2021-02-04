***
      PROGRAM mobseGUI
***
*
* Evolves a population of binaries using input parameters 
* read from input file binaries.in (M1, M2, P, e, Z, Tmax). 
*
***
      implicit none
*
      INCLUDE 'mobse/input/const_mobse.h'
*
      integer i,j,k,kk,jj,nsyst,met,countcheck
      integer kw,kw2,kwx,kwx2,kstar(2)
      integer i1,i2,kdum,id
*
      real*8 m1,m2,tmax,t
      real*8 mass0(2),mass(2),z,zpars(20)
      real*8 epoch(2),tms(2),tphys,tphysf,dtp
      real*8 rad(2),lum(2),ospin(2)
      real*8 massc(2),radc(2),menv(2),renv(2)
      real*8 sep0,tb0,tb,ecc0,ecc,aursun,yeardy,yearsc,tol
      PARAMETER(aursun=214.95d0,yeardy=365.25d0,yearsc=3.1557d+07)
      PARAMETER(tol=1.d-07)
      CHARACTER*8 label(14)
      real*8 t1,t2,mx,mx2,tbx,eccx
 
      INCLUDE 'input/parameters.h'
      INCLUDE 'input/binary.h'
*
* Open output files
      OPEN(20, file='output/mobse_long.out', status='unknown')
      WRITE(20,*)'time   m1   m2   type1   type2',
     &           '   logL1   logL2   logT1   logT2',
     &           '   logR1   logR2',
     &           '   sep   ecc'
      OPEN(21, file='output/mobse_label.out', status='unknown')
      WRITE(21,*)'time   m1   m2   type1   type2',
     &           '   logL1   logL2   logT1   logT2',
     &           '   logR1   logR2',
     &           '   sep   ecc   label'
*
* Set the seed for the random number generator. 
      if(idum.gt.0) idum = -idum
*
* Set the collision matrix.
      CALL instar
*
      label(1) = 'INITIAL '
      label(2) = 'KW_CHNGE'
      label(3) = 'BEG_RCHE'
      label(4) = 'END_RCHE'
      label(5) = 'CONTACT '
      label(6) = 'COELESCE'
      label(7) = 'COMENV  '
      label(8) = 'GNTAGE  '
      label(9) = 'NO_REMNT'
      label(10) = 'MAX_TIME'
      label(11) = 'DISRUPT '
      label(12) = 'BEG_SYMB'
      label(13) = 'END_SYMB'
      label(14) = 'BEG_BSS '
*
      CALL zcnsts(z,zpars)
*
      ecc0 = ecc
      tb0 = tb/yeardy
      sep0 = aursun*(tb0*tb0*(mass(1) + mass(2)))**(1.d0/3.d0)
      tb0 = tb
*
* Initialize the binary. 
      if(m1 .le. 0.7)then
            kstar(1) = 0
      else
      kstar(1) = 1
      endif
      mass0(1) = m1
      mass(1) = m1
      massc(1) = 0.d0
      ospin(1) = 0.d0
      epoch(1) = 0.d0
*
      if(m2 .le. 0.7)then
            kstar(2) = 0
      else
      kstar(2) = 1
      endif
      mass0(2) = m2
      mass(2) = m2
      massc(2) = 0.d0
      ospin(2) = 0.d0
      epoch(2) = 0.d0
*
      tphys = 0.d0
      tphysf = tmax
*
* Evolve the binary. 
      CALL evolve(kstar,mass0,mass,rad,lum,massc,radc,
     &               menv,renv,ospin,epoch,tms,
     &               tphys,tphysf,dtp,z,zpars,tb,ecc)
*
      jj = 1
* loop over bcm
      do while(bcm(jj,1).ge.0.0d0)
            kstar(1) = INT(bcm(jj,2))
            kstar(2) = INT(bcm(jj,16))
* print the jj step of the evolution
            write(20,180)bcm(jj,1),bcm(jj,4),bcm(jj,18),
     &         kstar(1),kstar(2),bcm(jj,5),bcm(jj,19),
     &         bcm(jj,7),bcm(jj,21),bcm(jj,6),bcm(jj,20),
     &         bcm(jj,31),bcm(jj,32)
*
            jj = jj + 1
      enddo
*
* loop over bpp
      j = 1
 52   j = j + 1
      if(bpp(j,1).lt.0.0) goto 60
            kstar(1) = INT(bpp(j,2))
            kstar(2) = INT(bpp(j,16))
            kw = INT(bpp(j,33))
            WRITE(21,181)bpp(j,1),bpp(j,4),bpp(j,18),
     &         kstar(1),kstar(2),bpp(j,5),bpp(j,19),
     &         bpp(j,7),bpp(j,21),bpp(j,6),bpp(j,20),
     &         bpp(j,31),bpp(j,32),label(kw)
            goto 52
 60   continue
*
 180  FORMAT(f11.4,2f9.4,1x,2i3,2f12.4,2x,2f12.4,2x,2e12.5,2x,
     &       2f12.4)
 181  FORMAT(f11.4,2f9.4,1x,2i3,2f12.4,2x,2f12.4,2x,2e12.5,2x,
     &       2f12.4,2x,a8)
*
* Close output
      CLOSE(20)
      CLOSE(21)
*
************************************************************************
      STOP
      END
***
