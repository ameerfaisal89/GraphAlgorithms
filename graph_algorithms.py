# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 02:19:56 2015

@author: Ameer Asif Khan
"""
#%%
import random;
import math;
from collections import deque;
from matplotlib import pyplot as plt;
import time;
import os;

os.chdir( "C:/Users/Ameer Asif Khan/My Documents/Academic/Northwestern/" + 
            "MSIA 490 Topics in Analytics in Python" );

#%%
class Vertex:
    '''
    Simulates each vertex in an undirected graph along with its attributes. The class
    attributes of the vertex include name, position and its neighbors stored as a
    dictionary of { neighbor vertex: weight }.
    '''
    def __init__( self, vName, vPos = ( 0, 0 ) ):
        '''
        The constructor for each Vertex instance
        '''
        self.name = vName;
        self.neighbors = { };
        self.pos = vPos;
    
    def __iter__( self ):
        return self;
    
    def __repr__( self ):
        return "V{0}".format( self.name );
    
    def __str__ ( self ):
        return ( self.__repr__( ) + ": Connected to [ " +
                ", ".join( [ v.__repr__( ) for v in self.getNeighbors( ) ] ) + " ]" );
    
    def addNeighbor( self, v, weight = 1 ):
        '''
        Adds another vertex object to the neighbor of the vertex. The value is the weight
        of the edge
        '''
        self.neighbors[ v ] = weight;
    
    def getNeighbors( self ):
        '''
        Returns an iterator over the neighbors of the vertex
        '''
        return iter( self.neighbors.keys( ) );
    
    def setRandomPosition( self ):
        '''
        Randomly assign position [0,1) to the vertex
        '''
        self.pos = ( random.random( ), random.random( ) );

class Graph:
    '''
    Simulates an undirected graph. The class is iterable over the vertices and also gives methods to
    iterate over the edges. The class attributes include the number of vertices, a dictionary of 
    vertex objects, and a dictionary of vertex pairs representing edges.
    '''
    def __init__( self, adjList = None ):
        '''
        Constructor creating an empty graph
        '''
        self.numVertices = 0;
        self.vertexList = { };
        self.edgeList = { };
    
    @classmethod
    def adjList( cls, adj ):
        obj = cls( );
        
        for edge in adj:
            uName = edge[ 0 ];
            vName = edge[ 1 ];
            
            obj.addVertex( uName );
            obj.addVertex( vName );
            
            if ( len( edge ) > 2 ):
                obj.addEdge( uName, vName, weight = edge[ 2 ] );
            elif ( len( edge ) == 2 ):
                obj.addEdge( uName, vName );
        
        return obj;
    
    @classmethod
    def randomGraph( cls, numVertices, numEdges, connected = False ):
        obj = cls( );
        
        for i in range( numVertices ):
            obj.addVertex( i );
        
        possibleEdges = int( ( numVertices * ( numVertices - 1 ) ) / 2 );
        
        if ( numEdges < possibleEdges ):
            j = 0;
            
            if ( connected and numEdges >= numVertices - 1 ):
                uList = [ ];
                vList = [ v.name for v in obj ];
                
                uList.append( vList.pop( ) );
                
                while ( len( vList ) > 0 ):
                    uName = uList[ random.randint( 0, len( uList ) - 1 ) ];
                    vName = vList.pop( random.randint( 0, len( vList ) - 1 ) );
                    uList.append( vName );
                    
                    obj.addEdge( uName, vName );
                    j += 1;
            elif ( connected ):
                raise RuntimeError;
            
            while ( j < numEdges ):
                uName = random.randint( 0, numVertices - 1 );
                vName = random.randint( 0, numVertices - 1 );
                
                if ( obj.addEdge( uName, vName ) ):
                    j += 1;
        
        elif ( numEdges == possibleEdges ):
            for j in range( numVertices - 1 ):
                uName = j;
                
                for k in range( j + 1, numVertices ):
                    vName = k;
                    obj.addEdge( uName, vName );
        
        else:
            raise RuntimeError;
        
        return obj;
    
    def vertices( self ):
        return iter( self.vertexList.values( ) );
    
    def edges( self ):
        return iter( self.edgeList.keys( ) );
    
    __iter__ = vertices;
    
    def addVertex( self, vName ):
        if ( vName not in self.vertexList ):
            self.vertexList[ vName ] = Vertex( vName );
            self.numVertices += 1;
            return True;
        else:
            return False;
    
    def addEdge( self, uName, vName, weight = 1 ):
        if ( ( uName not in self.vertexList ) or ( vName not in self.vertexList ) ):
            return False;
        
        u = self.vertexList[ uName ];
        v = self.vertexList[ vName ];
        
        if ( u is not v and v not in u.getNeighbors( ) ):
            u.addNeighbor( v, weight );
            v.addNeighbor( u, weight );
            
            if ( u.name < v.name ):
                self.edgeList[ ( u, v ) ] = weight;
            else:
                self.edgeList[ ( v, u ) ] = weight;
            return True;
        
        else:
            return False;
    
    def setDistanceWeight( self ):
        for u in self:
            u.visited = False;
        
        for u in self:
            for v in u.getNeighbors( ):
                if ( not v.visited ):
                    weight = 0;
                    
                    for i in range( 2 ):
                        diff = u.pos[ i ] - v.pos[ i ];
                        weight += diff * diff;
                    
                    weight = math.sqrt( weight );
                    
                    u.neighbors[ v ] = weight;
                    v.neighbors[ u ] = weight;
                    
                    if ( u.name < v.name ):
                        self.edgeList[ ( u, v ) ] = weight;
                    else:
                        self.edgeList[ ( v, u ) ] = weight;
            
            u.visited = True;
        
        for u in self:
            del u.visited;
    
    def scatterVertices( self ):
        for v in self:
            v.setRandomPosition( );
        
        self.setDistanceWeight( );
    
    def getComponents( self ):
        for v in self:
            v.visited = False;
        
        queue = deque( [ ] );
        component = 0;
        
        for u in self:
            if ( not u.visited ):
                u.visited = True;
                u.component = component;
                queue.append( u );
                
                while ( len( queue ) > 0 ):
                    v = queue.popleft( );
                    
                    for w in v.getNeighbors( ):
                        if ( not w.visited ):
                            w.visited = True;
                            w.component = component;
                            queue.append( w );
                
                component += 1;
        
        self.numComponents = component;
        
        for v in self:
            del v.visited;
    
    def minSpanningTree( self ):
        if ( not hasattr( self, "numComponents" ) ):
            self.getComponents( );
        
        if ( self.numComponents > 1 ):
            print( "Graph is not connected" );
            self.minSpanningTreeExists = False;
            return;
        
        for u in self:
            u.visited = False;
            u.treeNeighbors = [ ];
        
        eList = self.edgeList.copy( );
        
        root = random.choice( list( self.vertices( ) ) );
        root.visited = True;
        
        for _ in range( self.numVertices - 1 ):
            treeEdge = ( );
            minDist = float( "inf" );
            
            for e in eList:
                if ( eList[ e ] ):
                    u, v = e;
                    uFound = u.visited;
                    vFound = v.visited;
                    
                    if ( ( uFound and not vFound ) or ( not uFound and vFound ) ):
                        dist = eList[ e ];
                        if ( dist < minDist ):
                                minDist = dist;
                                treeEdge = e;
                    
                    elif ( uFound and vFound ):
                        eList[ e ] = None;
            
            u, v = treeEdge;
            u.treeNeighbors.append( v );
            v.treeNeighbors.append( u );
            
            u.visited = True;
            v.visited = True;
            eList[ treeEdge ] = None;
            
        for u in self:
            del u.visited;
        
        self.minSpanningTreeExists = True;
    
    def _plot( self, ax, plotTree = False ):
        pos_x = [ v.pos[ 0 ] for v in self ];
        pos_y = [ v.pos[ 1 ] for v in self ];
        comp = [ v.component for v in self ];
        
        ax.scatter( pos_x, pos_y, c = comp, s = 200, zorder = 2 );
        
        for u in self:
            for v in u.getNeighbors( ):
                if ( not plotTree or ( hasattr( u, "treeNeighbors" ) and v in u.treeNeighbors ) ):
                    edge = list( zip( u.pos, v.pos ) );
                    ax.plot( edge[ 0 ], edge[ 1 ], "k", zorder = 1 );
            
            ax.annotate( u.name, xy = u.pos, xytext = ( -10, 10 ), zorder = 3,
                         textcoords = 'offset points', ha = 'right', va = 'bottom',
                         bbox = dict( boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5 ),
                         arrowprops = dict( arrowstyle = '->', connectionstyle = 'arc3,rad=0' ) );
        
        ax.axis( "off" );
    
    def plot( self ):
        if ( not hasattr( self, "numComponents" ) ):
            self.getComponents( );
        
        f, ax = plt.subplots( );
        self._plot( ax );
        plt.title( "Graph" );
        plt.show( );
    
    def plotWithTree( self ):
        if ( not hasattr( self, "minSpanningTreeExists" ) ):
            self.minSpanningTree( );
        
        if ( not self.minSpanningTreeExists ):
            self.plot( );
            return;
        
        f, ( ax1, ax2 ) = plt.subplots( 1, 2 );
        self._plot( ax1 );
        self._plot( ax2, plotTree = True );
        plt.title( "Graph and its Minimum Spanning Tree" );
        plt.show( );
    
    def __str__( self ):
        return "\n".join( [ str( v ) for v in self ] );

#%%
def timer( func, init, nArray, rep = 10 ):
    timeLapse = [ 0 ] * len( nArray );
    
    for i, n in enumerate( nArray ):
        obj = init( n, 3 * n );
        
        for j in range( rep ):            
            startTime = time.process_time( );
            func( obj );
            timeLapse[ i ] += time.process_time( ) - startTime;
                    
        timeLapse[ i ] /= rep;
        print( '{0} time: n[ {1} ] = {2}'.format( func.__name__, n, timeLapse[ i ] ) );
    
    return timeLapse;

def initComponents( n, e ):
    obj = Graph.randomGraph( n, e );
    obj.scatterVertices( );
    return obj;

def initMST( n, e ):
    obj = Graph.randomGraph( n, e, True );
    obj.scatterVertices( );
    obj.getComponents( );
    return obj;

#%%
g = Graph( );

adjList = [ ( 2, 3 ), ( 2, 4 ), ( 1, 4 ), ( 3, 0 ), ( 0, 4 ), ( 1, 3 ) ];
g = Graph.adjList( adjList );

g = Graph.randomGraph( 20, 10 );
g.scatterVertices( );
g.getComponents( );
g.plot( );
g.minSpanningTree( );
g.plotWithTree( );

g = Graph.randomGraph( 10, 45, connected = True );
g.scatterVertices( );
g.getComponents( );
g.plot( );
g.minSpanningTree( );
g.plotWithTree( );

#%%
nArray = list( range( 1000, 10001, 1000 ) );
timeComponents = timer( Graph.getComponents, initComponents, nArray, 100 );

plt.plot( nArray, timeComponents, "-bo", label = "Connected Components" );
plt.title( "Time complexity for Breadth First Search" );
plt.xlabel( "Number of Vertices" );
plt.ylabel( "Time" );
plt.legend( loc = 1 );
plt.show( );

nArray = list( range( 200, 2001, 200 ) );
timeMST = timer( Graph.minSpanningTree2, initMST, nArray );

plt.plot( nArray, timeMST, "-bo", label = "Minimum Spanning Tree" );
plt.title( "Time complexity for Prim's Algorithm" );
plt.xlabel( "Number of Edges" );
plt.ylabel( "Time" );
plt.legend( loc = 1 );
plt.show( );
